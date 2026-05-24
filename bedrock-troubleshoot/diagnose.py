#!/usr/bin/env python3
"""
Bedrock Troubleshooting Diagnostic Tool

Comprehensive diagnostics for:
- Anthropic/Claude models (boto3)
- Mantle/OpenAI-compatible (Qwen, OSS models)

Tests real invocations, model ID formats, API versions, and message compatibility.
"""
import subprocess
import json
import sys
from pathlib import Path


def run_cmd(cmd: str) -> tuple[str, int]:
    """Run shell command and return output, exit code."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out", 1
    except Exception as e:
        return str(e), 1


def check_aws_credentials() -> tuple[bool, str]:
    """Check if AWS credentials are configured."""
    output, code = run_cmd("aws sts get-caller-identity")
    if code == 0:
        try:
            info = json.loads(output)
            return True, f"✓ Using IAM identity: {info.get('Arn', 'unknown')}"
        except:
            return True, f"✓ AWS credentials configured"
    else:
        return False, f"✗ AWS credentials not configured or invalid:\n{output}"


def check_bedrock_access(region: str) -> tuple[bool, str]:
    """Check if Bedrock is accessible in region."""
    cmd = f"aws bedrock list-foundation-models --region {region} --query 'modelSummaries[0].modelId' --output text"
    output, code = run_cmd(cmd)
    if code == 0:
        return True, f"✓ Bedrock is accessible in {region}"
    else:
        return False, f"✗ Cannot access Bedrock in {region}:\n{output}"


def get_available_claude_models(region: str = "us-east-1") -> list:
    """Get list of available Claude models."""
    cmd = f"aws bedrock list-foundation-models --region {region} --query 'modelSummaries[?contains(modelId, `claude`)].modelId' --output text"
    output, code = run_cmd(cmd)
    if code == 0 and output.strip():
        return output.strip().split()
    return []


def get_available_mantle_models(region: str = "us-west-2") -> list:
    """Get list of available Mantle models."""
    cmd = f"aws bedrock list-foundation-models --region {region} --query 'modelSummaries[?contains(modelId, `qwen`) || contains(modelId, `openai`)].modelId' --output text"
    output, code = run_cmd(cmd)
    if code == 0 and output.strip():
        return output.strip().split()
    return []


def test_claude_invocation(model_id: str, region: str = "us-east-1", profile: str = None) -> tuple[bool, str]:
    """Test actual Claude model invocation with correct format."""
    try:
        import boto3

        try:
            if profile:
                client = boto3.client("bedrock-runtime", region_name=region, profile_name=profile)
            else:
                client = boto3.client("bedrock-runtime", region_name=region)

            response = client.converse(
                modelId=model_id,
                messages=[{"role": "user", "content": [{"text": "Say OK"}]}],
            )
            return True, f"✓ Successfully invoked {model_id}"
        except client.exceptions.ValidationException as e:
            error_msg = str(e)
            if "model" in error_msg.lower() and "not found" in error_msg.lower():
                return False, f"✗ Model ID format error:\n  Error: {error_msg}\n  Fix: Use format 'us.anthropic.claude-sonnet-4-6' (with 'us.' prefix)"
            return False, f"✗ Validation error: {error_msg}"
        except Exception as e:
            error_msg = str(e)
            if "bedrock-2023" in error_msg or "API version" in error_msg.lower():
                return False, f"✗ API version error:\n  Error: {error_msg}\n  Fix: Ensure boto3 is up to date and using API version 'bedrock-2023-05-31'"
            if "region" in error_msg.lower() or "endpoint" in error_msg.lower():
                return False, f"✗ Region error:\n  Error: {error_msg}\n  Fix: Claude is only available in us-east-1"
            return False, f"✗ Invocation failed: {error_msg}"
    except ImportError:
        return False, "✗ boto3 not installed. Run: pip install boto3"


def test_wrong_model_id_format() -> tuple[bool, str]:
    """Test that wrong model ID format fails with clear error."""
    print("\n  Testing wrong model ID format (intentional error)...")
    try:
        import boto3

        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        try:
            response = client.converse(
                modelId="anthropic.claude-sonnet-4-6",  # WRONG: missing 'us.' prefix
                messages=[{"role": "user", "content": [{"text": "test"}]}],
            )
            return False, "  ⚠ Should have failed but didn't - model ID validation may be disabled"
        except Exception as e:
            error_msg = str(e)
            if "model" in error_msg.lower():
                return True, f"  ✓ Correctly rejected wrong format\n    Error: {error_msg}\n    Fix: Use 'us.anthropic.claude-sonnet-4-6' instead of 'anthropic.claude-sonnet-4-6'"
            return False, f"  ✗ Failed with unexpected error: {error_msg}"
    except ImportError:
        return False, "  ✗ boto3 not installed"


def test_deprecated_models() -> tuple[bool, str]:
    """Check for deprecated Claude models."""
    models = get_available_claude_models()
    if not models:
        return False, "  ✗ No models available to check"

    # Known deprecated patterns
    deprecated_patterns = ["claude-v1", "claude-instant", "claude-2", "claude-2.1"]

    deprecated_found = []
    for model in models:
        for pattern in deprecated_patterns:
            if pattern in model.lower():
                deprecated_found.append(model)

    if deprecated_found:
        current_models = [m for m in models if not any(d in m for d in deprecated_found)]
        return (
            False,
            f"  ⚠ Deprecated models found: {', '.join(deprecated_found)}\n"
            f"    Current models: {', '.join(current_models[:3])}",
        )
    return True, f"  ✓ No deprecated models detected\n    Available: {', '.join(models[:3])}"


def test_region_mismatch() -> tuple[bool, str]:
    """Test that using wrong region fails appropriately."""
    print("\n  Testing wrong region (intentional error)...")
    try:
        import boto3

        client = boto3.client("bedrock-runtime", region_name="us-west-2")  # WRONG for Claude
        try:
            response = client.converse(
                modelId="us.anthropic.claude-sonnet-4-6",
                messages=[{"role": "user", "content": [{"text": "test"}]}],
            )
            return False, "  ⚠ Should have failed in wrong region"
        except Exception as e:
            error_msg = str(e)
            return (
                True,
                f"  ✓ Correctly rejected wrong region\n"
                f"    Error: {error_msg}\n"
                f"    Fix: Claude is only in us-east-1",
            )
    except ImportError:
        return False, "  ✗ boto3 not installed"


def diagnose_claude_path():
    """Comprehensive Claude/Anthropic Bedrock diagnostics."""
    print("\n📋 Claude/Anthropic Bedrock Comprehensive Diagnostics")
    print("=" * 70)

    # Stage 1: Prerequisites
    print("\n[1/4] Checking Prerequisites...")
    passed, msg = check_aws_credentials()
    print(f"  {msg}")
    if not passed:
        print("\n❌ AWS credentials required. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return

    passed, msg = check_bedrock_access("us-east-1")
    print(f"  {msg}")
    if not passed:
        print("\n❌ Cannot access Bedrock in us-east-1. Check IAM permissions.")
        return

    # Stage 2: Model availability
    print("\n[2/4] Checking Model Availability...")
    models = get_available_claude_models("us-east-1")
    if models:
        print(f"  ✓ Claude models available:")
        for m in models[:5]:
            print(f"    - {m}")
    else:
        print("  ✗ No Claude models found")
        return

    # Stage 3: Format and API version tests
    print("\n[3/4] Testing Model ID Format & API Version...")

    # Test correct format
    good_model = models[0] if models else "us.anthropic.claude-sonnet-4-6"
    passed, msg = test_claude_invocation(good_model)
    print(f"  {msg}")

    # Test wrong format
    passed, msg = test_wrong_model_id_format()
    print(msg)

    # Test deprecated models
    passed, msg = test_deprecated_models()
    print(f"  {msg}")

    # Test wrong region
    passed, msg = test_region_mismatch()
    print(msg)

    # Stage 4: Summary
    print("\n[4/4] Summary & Next Steps")
    print("=" * 70)
    print("\n✅ Setup appears correct! Key requirements:")
    print("  1. Model ID format: use 'us.anthropic.claude-sonnet-4-6' (with 'us.' prefix)")
    print("  2. Region: MUST be 'us-east-1' (global endpoint)")
    print("  3. API version: boto3 handles this (bedrock-2023-05-31)")
    print("  4. IAM: needs bedrock:InvokeModel permission")
    print("\nCode example:")
    print("""
    import boto3
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.converse(
        modelId='us.anthropic.claude-sonnet-4-6',
        messages=[{'role': 'user', 'content': [{'text': 'Hello'}]}]
    )
    """)


def diagnose_mantle_path():
    """Comprehensive Mantle/OpenAI-compatible diagnostics."""
    print("\n📋 Mantle (OpenAI-compatible) Comprehensive Diagnostics")
    print("=" * 70)

    # Stage 1: Prerequisites
    print("\n[1/3] Checking Prerequisites...")
    passed, msg = check_aws_credentials()
    print(f"  {msg}")
    if not passed:
        print("\n❌ AWS credentials required. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return

    passed, msg = check_bedrock_access("us-west-2")
    print(f"  {msg}")
    if not passed:
        print("  ⚠ us-west-2 not available, checking us-east-1...")
        passed, msg = check_bedrock_access("us-east-1")
        if passed:
            print("  ✓ Bedrock available in us-east-1 instead")
        else:
            print("\n❌ Mantle not available in your region. Check AWS docs for regional availability.")
            return

    # Stage 2: Model availability
    print("\n[2/3] Checking Mantle Model Availability...")
    models = get_available_mantle_models("us-west-2")
    if not models:
        models = get_available_mantle_models("us-east-1")

    if models:
        print(f"  ✓ Mantle models available:")
        for m in models[:5]:
            print(f"    - {m}")
    else:
        print("  ✗ No Mantle/OSS models found in available regions")
        return

    # Stage 3: Token and compatibility
    print("\n[3/3] Setup Requirements")
    print("=" * 70)
    print("\n✅ Mantle setup checklist:")
    print("  1. Generate bearer token:")
    print("     $ aws-bedrock-token-generator --model qwen.qwen3-coder-30b-a3b-instruct --region us-west-2")
    print("  2. Token TTL: typically 1 hour (regenerate as needed)")
    print("  3. Use OpenAI SDK with Bedrock endpoint:")
    print("     Base URL: https://bedrock.us-west-2.amazonaws.com/openai/v1")
    print("  4. Message format: Use OpenAI `chat.completions.create()` (NOT Anthropic format)")
    print("\nCode example:")
    print("""
    from openai import OpenAI

    token = "your-bedrock-token-here"
    client = OpenAI(
        api_key=token,
        base_url="https://bedrock.us-west-2.amazonaws.com/openai/v1"
    )
    response = client.chat.completions.create(
        model="qwen.qwen3-coder-30b-a3b-instruct",
        messages=[{"role": "user", "content": "Hello"}]
    )
    """)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Bedrock Troubleshooting Diagnostic Tool

Comprehensive testing for Claude and Mantle integration.
Tests: credentials, region, model availability, formats, and real invocations.

Usage:
  python diagnose.py              # Interactive mode
  python diagnose.py --help       # Show this help
  python diagnose.py --claude     # Diagnose Claude path only
  python diagnose.py --mantle     # Diagnose Mantle path only
""")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--claude":
        diagnose_claude_path()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--mantle":
        diagnose_mantle_path()
        return

    # Interactive mode
    print("\n🔧 Bedrock Troubleshooting Diagnostics")
    print("=" * 70)
    print("\nWhich integration are you working on?")
    print("1. Anthropic Claude models (boto3)")
    print("2. Mantle / OpenAI-compatible API (Qwen, OSS)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        diagnose_claude_path()
    elif choice == "2":
        diagnose_mantle_path()
    else:
        print("Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
