import streamlit as st
import hashlib
import time
import math
import re

# ==========================================
# MODULE 1: DICTIONARY GENERATOR & MUTATION
# ==========================================
def generate_dictionary(base_word, add_year=True, leet_speak=False):
    wordlist = set([base_word])
    mutations = []
    
    mutations.append(base_word.lower())
    mutations.append(base_word.upper())
    mutations.append(base_word.capitalize())
    
    if leet_speak:
        leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '\$', 't': '7'}
        for word in list(mutations):
            leet_word = "".join(leet_map.get(c.lower(), c) for c in word)
            mutations.append(leet_word)
            
    for word in mutations:
        wordlist.add(word)
        if add_year:
            wordlist.add(f"{word}123")
            wordlist.add(f"{word}2026")
            wordlist.add(f"{word}!")
            
    return sorted(list(wordlist))

# ==========================================
# MODULE 2: HASH EXTRACTION & IDENTIFIER
# ==========================================
def simulate_hash_extraction():
    return [
        {"User": "root", "Source": "Linux (/etc/shadow)", "Type": "SHA-512 (6)", "Hash": "\$6saltsalt9A8b7C..."},
        {"User": "Administrator", "Source": "Windows SAM Hive", "Type": "NTLM", "Hash": "aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0"},
        {"User": "legacy_user", "Source": "Database Backup", "Type": "MD5", "Hash": "5d41402abc4b2a76b9719d911017c592"}
    ]

# ==========================================
# MODULE 3 & 4: CRACKING ENGINE & ANALYZER
# ==========================================
def calculate_entropy(password):
    if not password:
        return 0
    pool = 0
    if re.search(r'[a-z]', password): pool += 26
    if re.search(r'[A-Z]', password): pool += 26
    if re.search(r'[0-9]', password): pool += 10
    if re.search(r'[^a-zA-Z0-9]', password): pool += 32
    
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    return round(entropy, 2)

def evaluate_strength(password, entropy):
    if len(password) < 8 or entropy < 40:
        return "🔴 WEAK (High risk of instant compromise)", "Enforce minimum length of 12 characters and mix special character pools."
    elif len(password) < 12 or entropy < 60:
        return "🟡 MEDIUM (Vulnerable to dedicated dictionary rule matching)", "Incorporate uppercase characters and non-standard keyboard patterns."
    else:
        return "🟢 STRONG (Excellent structural defense)", "Maintain active rotation intervals and monitor authentication log trends."

# ==========================================
# MODULE 5: STREAMLIT FRONTEND USER INTERFACE
# ==========================================
st.set_page_config(page_title="Credential Attack Suite", page_icon="🔑", layout="wide")

st.title("🔑 Password Cracking & Credential Attack Suite")
st.markdown("### Ethical Red-Team Auditing & Blue-Team Authentication Defense Simulation Dashboard")

tab1, tab2, tab3 = st.tabs(["⚙️ Dictionary & Cracking Engine", "📦 Hash Extraction Vault", "🛡️ Policy Strength Analyzer"])

with tab1:
    st.header("Custom Wordlist Generator & Attack Simulator")
    col1, col2 = st.columns(2)
    
    with col1:
        base_input = st.text_input("Enter target base word (e.g., name or company):", "admin")
        use_leet = st.checkbox("Enable Leet-Speak Mutations (e.g., a -> @, e -> 3)")
        use_suffix = st.checkbox("Append common numeric suffixes (+123, +2026)", value=True)
        
        generated_words = generate_dictionary(base_input, use_suffix, use_leet)
        st.success(f"Generated {len(generated_words)} mutated wordlist targets!")
        st.text_area("Generated Wordlist Preview:", "\n".join(generated_words), height=150)
        
    with col2:
        st.subheader("Simulate Dictionary Exhaustion Crack")
        target_password = st.text_input("Set a target plaintext password to simulate intercept:", "Adm1n2026")
        target_hash = hashlib.sha256(target_password.encode()).hexdigest()
        st.info(f"Target SHA-256 Signature: {target_hash}")
        
        if st.button("🚀 Run Auditing Simulation"):
            found = False
            start_time = time.time()
            
            for index, guess in enumerate(generated_words):
                guess_hash = hashlib.sha256(guess.encode()).hexdigest()
                if guess_hash == target_hash:
                    duration = time.time() - start_time
                    st.success(f"🎯 MATCH FOUND! Cracked password is: **{guess}**")
                    st.metric("Attempts Checked", index + 1)
                    st.metric("Time Taken", f"{duration:.6f} seconds")
                    found = True
                    break
            if not found:
                st.error("Cracking simulation complete. Target password was not found in the custom mutated wordlist registry.")


  
with tab2:
    st.header("Hash Extraction & Format Identification Lab")
    st.markdown(
        "Upload a text or CSV file containing synthetic lab records. "
        "This demo identifies hash formats; it does not extract credentials "
        "from protected operating-system files."
    )

    uploaded_file = st.file_uploader(
        "Upload synthetic hash records (.txt or .csv)",
        type=["txt", "csv"],
        key="lab_hash_upload"
    )

    def identify_hash_format(value):
        value = value.strip()

        if value.startswith("$6$"):
            return "SHA-512 crypt (format signature)"
        elif value.startswith("$5$"):
            return "SHA-256 crypt (format signature)"
        elif len(value) == 32 and all(
            c in "0123456789abcdefABCDEF" for c in value
        ):
            return "Possible MD5 (length-based guess)"
        elif len(value) == 64 and all(
            c in "0123456789abcdefABCDEF" for c in value
        ):
            return "Possible SHA-256 (length-based guess)"
        elif len(value) == 40 and all(
            c in "0123456789abcdefABCDEF" for c in value
        ):
            return "Possible SHA-1 (length-based guess)"
        else:
            return "Unknown or unsupported format"

    if uploaded_file is not None:
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            records = []

            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",") if "," in line else line.split(":")
                if len(parts) < 2:
                    continue

                username = parts[0].strip()
                hash_value = parts[-1].strip()

                if username.lower() in {"user", "username"}:
                    continue

                records.append({
                    "User": username,
                    "Hash Preview": (
                        hash_value[:12] + "..."
                        if len(hash_value) > 12 else hash_value
                    ),
                    "Detected Format": identify_hash_format(hash_value)
                })

            if records:
                st.success(f"Processed {len(records)} lab record(s).")
                st.dataframe(records, use_container_width=True)
                st.download_button(
                    "Download format analysis",
                    data=__import__("json").dumps(records, indent=2),
                    file_name="hash_format_analysis.json",
                    mime="application/json"
                )
            else:
                st.warning(
                    "No records were recognized. Use one synthetic "
                    "username,hash-value pair per line."
                )

        except UnicodeDecodeError:
            st.error("Please upload a UTF-8 encoded text or CSV file.")

    else:
        st.info("Upload a synthetic lab file to begin format identification.")
        st.code(
            "lab_user,5d41402abc4b2a76b9719d911017c592\n"
            "demo_user,"
            "e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855",
            language="text"
        )

    st.caption(
        "Format detection is heuristic, not proof of the algorithm. "
        "Different algorithms can produce hashes of the same length."
    )


with tab3:
    st.header("Cryptographic Password Entropy & Complexity Analyzer")
    check_pass = st.text_input("Input custom string value to audit:", "Security_2026!")
    
    if check_pass:
        entropy_score = calculate_entropy(check_pass)
        rating, fix = evaluate_strength(check_pass, entropy_score)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Password Length", f"{len(check_pass)} characters")
        c2.metric("Calculated Entropy Score", f"{entropy_score} Bits")
        c3.markdown(f"**Security Profiling:** {rating}")
        
        hash_rate = 10_000_000_000
        total_combinations = math.pow(2, entropy_score)
        seconds_to_crack = total_combinations / hash_rate
        
        st.subheader("📊 Theoretical Brute Force Exhaustion Threshold")
        if seconds_to_crack < 1:
            st.error("Estimated Cracking Frame: **Instantaneous (Less than 1 second)**")
        elif seconds_to_crack < 86400:
            st.warning(f"Estimated Cracking Frame: **~{seconds_to_crack/3600:.2f} Hours**")
        else:
            st.success(f"Estimated Cracking Frame: **~{seconds_to_crack/31536000:.2f} Years**")
            
        st.markdown(f"**🛡️ Remediation Advice:** {fix}")

st.markdown("---")
st.subheader("📥 Export Production Security Audit Report")
report_data = f"""PASSWORD SECURITY AUDIT LOG EXPORT
------------------------------------------
Total Audit Matrix Scope: Entropy & Wordlist Verification
Target Sample Evaluated Length: {len(check_pass)}
Calculated Bit Entropy Pool: {calculate_entropy(check_pass)}
Recommended Baseline: Enforce minimum 14-character length with random salts.
"""
st.download_button(label="📄 Download Security Audit Dataset Report (.txt)", data=report_data, file_name="Password_Audit_Report.txt")
