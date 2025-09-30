#!/bin/bash
# Quick test script for Parakeet model

echo "========================================="
echo "Wispr-Flow Clone - Parakeet GPU Test"
echo "========================================="
echo ""

echo "1. Checking PyTorch CUDA..."
.venv/bin/python -c "import torch; print(f'   CUDA available: {torch.cuda.is_available()}'); print(f'   GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
echo ""

echo "2. Checking NeMo..."
.venv/bin/python -c "import nemo.collections.asr as nemo_asr; print('   NeMo ASR: OK')" 2>/dev/null && echo "   ✓ NeMo installed" || echo "   ✗ NeMo not found"
echo ""

echo "3. Current configuration:"
echo "   Model type: $(grep 'type:' config.yaml | head -1 | awk '{print $2}')"
echo "   Model size: $(grep 'size:' config.yaml | head -1 | awk '{print $2}')"
echo "   Device: $(grep 'device:' config.yaml | head -1 | awk '{print $2}')"
echo ""

echo "4. GPU Status:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader | awk -F', ' '{print "   " $0}'
echo ""

echo "========================================="
echo "Ready to test!"
echo ""
echo "Run:  ./run.sh"
echo "Then: Press Ctrl+Alt and speak"
echo "========================================="
