# 📝 What is `.gitkeep` and Why Use It?

By default, Git does not track empty folders — it only tracks files.

However, in many projects, it is important to keep certain folders in the repository even when they're empty. This is especially useful for folders like:

- `logs/` – for runtime logs
- `data/raw/` – for raw data files
- `notebooks/` – for future notebooks
- `exports/` – for outputs like CSVs or images

## ✅ Solution: `.gitkeep`

To make sure these folders are included in the Git repository and appear on GitHub, we place an empty file named `.gitkeep` inside them.

This file has **no functional purpose** in the code. It is only a placeholder to tell Git:  
👉 _“Track this folder, even if it’s empty.”_

## 📌 Note

`.gitkeep` is **not an official Git feature**, just a widely adopted naming convention. You could name the file anything (`.placeholder`, `empty.txt`), but `.gitkeep` is the most recognized.

---

✅ Summary:  
- Git ignores empty folders.  
- `.gitkeep` is a trick to force Git to track them.  
- This improves folder structure clarity and consistency across collaborators.