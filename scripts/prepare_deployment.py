#!/usr/bin/env python3
"""
Pre-deployment script to prepare the project for Streamlit Cloud.

This script:
1. Runs the full pipeline to generate data, models, and warehouse
2. Verifies all required files exist
3. Checks file sizes for deployment limits
4. Provides git commands to commit deployment artifacts
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a shell command and return success status."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
        return True
    else:
        print(f"❌ {description} - FAILED")
        return False


def check_file_size(filepath: Path) -> tuple[bool, float]:
    """Check if file exists and return size in MB."""
    if not filepath.exists():
        return False, 0.0
    size_mb = filepath.stat().st_size / (1024 * 1024)
    return True, size_mb


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 Streamlit Cloud Deployment Preparation Script          ║
║                                                              ║
║   This will prepare your Hospital Data Insights Pipeline    ║
║   for deployment to Streamlit Community Cloud               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    root = Path(__file__).parent
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("\n⚠️  Failed to install dependencies. Please check your requirements.txt")
        return 1
    
    # Step 2: Run the pipeline
    if not run_command(
        "python scripts/run_all.py",
        "Running data pipeline (this may take a few minutes)"
    ):
        print("\n⚠️  Pipeline failed. Please check the errors above.")
        return 1
    
    # Step 3: Verify required files
    print(f"\n{'='*60}")
    print("📁 Verifying required files for deployment")
    print(f"{'='*60}\n")
    
    required_files = {
        "Config": root / "config.yaml",
        "Dashboard": root / "dashboard" / "app.py",
        "Requirements": root / "requirements.txt",
        "Streamlit Config": root / ".streamlit" / "config.toml",
        "Database": root / "warehouse" / "hospital.duckdb",
    }
    
    all_exist = True
    for name, filepath in required_files.items():
        exists, size = check_file_size(filepath)
        if exists:
            print(f"✅ {name:20s}: {filepath.name:30s} ({size:.2f} MB)")
        else:
            print(f"❌ {name:20s}: {filepath.name:30s} MISSING!")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some required files are missing. Please check the errors above.")
        return 1
    
    # Step 4: Check data files
    print(f"\n{'='*60}")
    print("📊 Checking processed data files")
    print(f"{'='*60}\n")
    
    data_dir = root / "data" / "processed"
    data_files = list(data_dir.glob("*.csv"))
    total_data_size = 0
    
    for filepath in sorted(data_files):
        exists, size = check_file_size(filepath)
        total_data_size += size
        print(f"  {filepath.name:40s} {size:8.2f} MB")
    
    # Step 5: Check model files
    print(f"\n{'='*60}")
    print("🤖 Checking model files")
    print(f"{'='*60}\n")
    
    model_dir = root / "models"
    model_files = list(model_dir.glob("*.joblib")) + list(model_dir.glob("*.json"))
    total_model_size = 0
    
    for filepath in sorted(model_files):
        exists, size = check_file_size(filepath)
        total_model_size += size
        print(f"  {filepath.name:40s} {size:8.2f} MB")
    
    # Step 6: Check total size
    db_exists, db_size = check_file_size(root / "warehouse" / "hospital.duckdb")
    total_size = total_data_size + total_model_size + db_size
    
    print(f"\n{'='*60}")
    print("📦 Deployment Package Summary")
    print(f"{'='*60}\n")
    print(f"  Processed Data:  {total_data_size:8.2f} MB")
    print(f"  Models:          {total_model_size:8.2f} MB")
    print(f"  Database:        {db_size:8.2f} MB")
    print(f"  {'─'*40}")
    print(f"  Total Size:      {total_size:8.2f} MB")
    
    if total_size > 100:
        print(f"\n⚠️  WARNING: Total size ({total_size:.2f} MB) exceeds GitHub's 100MB file limit!")
        print("   Consider:")
        print("   1. Using Git LFS for large files")
        print("   2. Reducing synthetic data size in config.yaml")
        print("   3. Compressing the database")
    else:
        print(f"\n✅ Total size is within limits!")
    
    # Step 7: Provide git commands
    print(f"\n{'='*60}")
    print("📝 Next Steps: Commit to Git")
    print(f"{'='*60}\n")
    print("Run these commands to commit your deployment files:\n")
    print("  # Add all deployment files")
    print("  git add .")
    print("  git add -f data/processed/*.csv")
    print("  git add -f models/*.joblib models/*.json")
    print("  git add -f warehouse/hospital.duckdb")
    print("")
    print("  # Commit the changes")
    print("  git commit -m \"Prepare for Streamlit Cloud deployment\"")
    print("")
    print("  # Push to GitHub")
    print("  git push origin main")
    print("")
    print("Then follow the instructions in DEPLOYMENT.md!")
    print("")
    
    print("✨ Preparation complete! Ready for deployment! ✨\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
