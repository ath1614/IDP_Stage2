import surya
import inspect
print(f"Surya file: {surya.__file__}")
print(f"Dir surya: {dir(surya)}")
try:
    import surya.ocr
    print("surya.ocr found")
    print(dir(surya.ocr))
except ImportError as e:
    print(f"Error importing surya.ocr: {e}")

try:
    from surya.ocr import run_ocr
    print("run_ocr found")
except ImportError:
    print("run_ocr NOT found in surya.ocr")
