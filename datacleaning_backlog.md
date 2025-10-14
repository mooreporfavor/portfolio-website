### **Data Cleaning Backlog**

#### **Priority 1: Critical Integrity Issues (Must Fix)**

These items will corrupt your `CVvault` by introducing duplicate or irrelevant data. They should be fixed before running the full AI pipeline.
*   **Task:** Remove exact duplicate files.
    *   **Files:**
        *   `Cover Letter - WB Education ES - Ryan Moore (1).pdf` (Duplicate of the one above it)
        *   `CV - GCF Strategy - Ryan Moore.pdf` (Appears multiple times)
        *   `CV - IADB OVE - Ryan Moore.pdf` (Appears multiple times)
        *   `Cover Letter - OSP - Ryan Moore.docx (Converted - ...)` (Appears twice)
        *   `Cover Letter - MCC A&F SrAdv - Ryan Moore.docx (Converted - ...)` (Appears twice)
    *   **Reason:** Duplicates will cause the AI to over-weigh the content in those files.
    *   **Action:** **Review and delete** the redundant copies.

---

#### **Priority 2: Content Extraction Failures (High Priority)**

These are files that your script attempted to read but failed, resulting in no usable text.

*   **Task:** Standardize and repair `.docx` and extensionless files that failed to parse.
    *   **Files:**
        *   `CV - Rockefeller AI - Ryan Moore`
        *   `CV - IDB Education - Ryan Moore.docx`
        *   `CV and References - Gates DD Education - Ryan Moore.docx`
        *   `CV - GCF Strategy - Ryan Moore`
        *   `CV - 2025 - Ryan Moore`
        *   `CV - CGD Policy Fellow - Ryan Moore.docx`
        *   `CV - GCF Financing - Ryan Moore.docx`
    *   **Reason:** These are likely old `.doc` formats or malformed Word files that the parser cannot read.
    *   **Action:** For each file, **use the "Open with -> Google Docs" trick** to create a clean, native Google Doc version. Then, delete the original problematic file.

---

#### **Priority 3: Unsupported File Types (Medium Priority)**

These files are currently being ignored by the script.

*   **Task:** Convert unsupported file formats to a readable format.
    *   **Files:**
        *   `Cover Letter - GCF - Ryan Moore.txt`
        *   `CV and References - 2025 - DPT - Ryan Moore.odt`
    *   **Reason:** The script doesn't have a parser for `.txt` or `.odt` files.
    *   **Action:** **Manually open each file**, copy its content, and **paste it into a new Google Doc** within the same folder. Then, delete the original unsupported file.