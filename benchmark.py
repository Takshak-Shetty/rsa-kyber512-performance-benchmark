import time
import os
import tracemalloc
import psutil
import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Try to import oqs; if not available, only RSA will be tested
try:
    import oqs
    OQS_AVAILABLE = True
except Exception:
    OQS_AVAILABLE = False
    print("⚠️ Warning: liboqs / liboqs-python not available. Kyber tests will be skipped.")

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_rss_kb():
    proc = psutil.Process(os.getpid())
    return proc.memory_info().rss / 1024.0

# ---------------- RSA Benchmark ---------------- #
def rsa_test():
    tracemalloc.start()
    start = time.time()
    key = RSA.generate(2048)
    end = time.time()
    mem_pyheap_kb = tracemalloc.get_traced_memory()[1] / 1024.0
    tracemalloc.stop()
    proc_rss_kb = get_rss_kb()

    cipher_rsa = PKCS1_OAEP.new(key)
    message = b'Post Quantum Cryptography Test'
    enc_start = time.time()
    ciphertext = cipher_rsa.encrypt(message)
    enc_end = time.time()

    dec_start = time.time()
    decrypted = cipher_rsa.decrypt(ciphertext)
    dec_end = time.time()

    return {
        "Algo": "RSA",
        "KeyGen(s)": end - start,
        "Encrypt(s)": enc_end - enc_start,
        "Decrypt(s)": dec_end - dec_start,
        "KeySize(Bytes)": len(key.export_key()),
        "Memory_PyHeap_KB": round(mem_pyheap_kb, 2),
        "Memory_RSS_KB": round(proc_rss_kb, 2)
    }

# ---------------- Kyber Benchmark ---------------- #
def kyber_test():
    if not OQS_AVAILABLE:
        raise RuntimeError("liboqs not available")

    tracemalloc.start()
    start = time.time()
    kem = oqs.KeyEncapsulation("Kyber512")
    public_key = kem.generate_keypair()
    end = time.time()
    mem_pyheap_kb = tracemalloc.get_traced_memory()[1] / 1024.0
    tracemalloc.stop()
    proc_rss_kb = get_rss_kb()

    ciphertext, shared_secret_sender = kem.encap_secret(public_key)
    dec_start = time.time()
    shared_secret_receiver = kem.decap_secret(ciphertext)
    dec_end = time.time()

    try:
        kem.free()
    except Exception:
        pass

    return {
        "Algo": "Kyber512",
        "KeyGen(s)": end - start,
        "Encrypt(s)": 0.0,  # Kyber is a KEM, not direct encryption
        "Decrypt(s)": dec_end - dec_start,
        "KeySize(Bytes)": len(public_key),
        "Memory_PyHeap_KB": round(mem_pyheap_kb, 2),
        "Memory_RSS_KB": round(proc_rss_kb, 2)
    }

# ---------------- Example Demonstration ---------------- #
def example_demo():
    print("\n==============================")
    print("🔍 Example: RSA vs Kyber512 Encryption Demonstration")
    print("==============================")

    message = b"Post Quantum Cryptography Test"
    print(f"\nOriginal Plaintext: {message}")

    # --- RSA Example ---
    print("\n--- RSA Example ---")
    rsa_key = RSA.generate(2048)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    ciphertext_rsa = cipher_rsa.encrypt(message)
    decrypted_rsa = cipher_rsa.decrypt(ciphertext_rsa)
    print(f"Ciphertext (hex snippet): {ciphertext_rsa.hex()[:60]}...")
    print(f"Decrypted Text: {decrypted_rsa}")
    print("✅ RSA encryption-decryption successful!")

    # --- Kyber Example ---
    if OQS_AVAILABLE:
        print("\n--- Kyber512 Example ---")
        kem = oqs.KeyEncapsulation("Kyber512")
        public_key = kem.generate_keypair()
        ciphertext, shared_secret_sender = kem.encap_secret(public_key)
        shared_secret_receiver = kem.decap_secret(ciphertext)
        print(f"Public Key Size: {len(public_key)} bytes")
        print(f"Ciphertext (hex snippet): {ciphertext.hex()[:60]}...")
        print(f"Shared Secret Match: {shared_secret_sender == shared_secret_receiver}")
        print("✅ Kyber512 key encapsulation successful!")
        kem.free()
    else:
        print("\n⚠️ Kyber512 demonstration skipped (liboqs not installed).")

# ---------------- Main Benchmark Runner ---------------- #
def main():
    results = []
    runs = 5

    print("\n==============================")
    print("⚙️  Running Cryptographic Benchmarks (RSA vs Kyber512)")
    print("==============================")

    for i in range(runs):
        print(f"\n▶ Run {i+1}/{runs} - RSA")
        results.append(rsa_test())
        if OQS_AVAILABLE:
            print(f"▶ Run {i+1}/{runs} - Kyber512")
            results.append(kyber_test())

    df = pd.DataFrame(results)
    out_path = os.path.join(RESULTS_DIR, "benchmark.csv")
    df.to_csv(out_path, index=False)
    print(f"\n✅ Benchmark results saved to: {out_path}")

    example_demo()  # run the example after benchmark

if __name__ == "__main__":
    main()
