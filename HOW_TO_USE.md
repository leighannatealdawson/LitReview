# 🐾 The Magical Species Finder 🧬
### *For PhD students who'd rather not read 500 papers to find out what animals they mention*

---

## 🎯 What This Thing Does

Remember when you had to read through tons of research papers and manually note down every time someone mentioned "*Polar bear*" or "*E. coli*"? Yeah, those days are **OVER**! 🎉

This little AI wizard reads your papers and automatically finds all the species names for you. It's like having a really smart research assistant who never needs coffee breaks.

---

## 🛠️ Setup 

### Step 1: Get Python on Your Computer 🐍

1. Go to [python.org/downloads](https://python.org/downloads)
2. Download the latest Python (the big blue button)
3. **SUPER IMPORTANT:** When installing, check the box that says "Add Python to PATH"
   *(This is giving Python permission to work everywhere on your computer)*
4. Let it install and grab a coffee ☕

**Test if it worked:**
- Press `Win + R`, type `cmd`, hit Enter
- Type: `python --version`
- If you see something like "Python 3.11.x" - you're golden! 🌟
- If you get an error, try `py --version` instead

### Step 2: Find Your Project Folder 📁
**This should be rather easy**

Put the LitReview folder somewhere you can remember. Like your Desktop. Your future self will thank you.

### Step 3: The One-Button Setup ✨
**Here comes the fun part!**

1. **Open Command Prompt** (Press `Win + R`, type `cmd`, hit Enter)
2. **Navigate to your folder:**
   ```cmd
   cd C:\Users\YourName\Desktop\LitReview
   ```
   **Pro tip:** Just drag the LitReview folder into the black window and it'll type the path for you! 🪄

3. **Run the magical setup spell:**
   ```cmd
   python info\setup.py
   ```

4. **Wait and watch the magic happen** ⏰
   - It'll download TaxoNERD (the AI brain that knows about species)
   - Download some language models (~1GB - good time for a snack break)
   - Set up everything automatically
   - Takes about 5-10 minutes

5. **When you see "🎉 Setup complete!" you're done!**

---

## 🚀 How to Use It

### Every Time You Want to Extract Species:

**Step 1: Wake Up the Magic Environment** (you can skip the cd .../LitReview if you open your terminal already in that folder)
```cmd
cd C:\Users\YourName\Desktop\LitReview
venv\Scripts\activate
``` 
*You'll see `(venv)` appear - this means the magic is active! ✨*

**Step 2: Put Your CSV File in the Right Place**
- Drop your literature CSV into the `data\input\` folder
- Name it something sensible like `martes_martes_papers.csv` (not `untitled1.csv` 😅)

**Step 3: run the actual script that does something**
*Little bit of info*
python <- Tell your terminal what we want to use 
scripts/extract_species.py <- this is script
data/input/your_file.csv <- input file

```cmd
python scripts\extract_species.py data\input\your_file.csv
```

**Step 4: Go Make Tea While the AI Works** 🍵
*Seriously, this takes a few minutes. The AI is reading every word and thinking "Hmm, is this a species name?"*

**Step 5: Check Your Results!**
Look in `data\output\` - you'll find:
- Your original CSV with species added
- A summary of all species found across all papers

---

## 📊 What You Get Back

### Main Results File:
Your CSV with fancy new columns:
- `extracted_species`: All the critters found in that paper
- `species_count`: How many different species mentioned

### Species Summary File:
A ranked list showing:
- Which species appear across your entire literature collection
- How often each one is mentioned
- Perfect for spotting research trends! 📈

---

## 🎨 Customizing Your Magic

### If your text is in a different column:
```cmd
python scripts\extract_species.py data\input\your_file.csv --text-column title
```

### Save somewhere specific:
```cmd
python scripts\extract_species.py data\input\your_file.csv --output data\output\my_awesome_results.csv
```

---

## 🆘 When Things Go Wrong (Don't Panic!)

### "Python is not recognized" 😱
- **Translation:** Windows doesn't know where Python lives
- **Fix:** Reinstall Python and CHECK that "Add to PATH" box
- **Alternative:** Try typing `py` instead of `python`

### "I can't find my files!" 📂
**Check what's in your input folder:**
```cmd
dir data\input
```

### "The script is taking FOREVER!" ⏰
- **This is normal!** AI analysis is slow but thorough
- Expect 1-2 minutes per 10 papers
- Perfect time to:
  - Make tea ☕
  - Check Instagram 📱
  - Contemplate the meaning of life 🤔
  - Or just watch the progress messages scroll by

### "Column 'abstract' not found" 🤯
**Your CSV columns have different names. Check what you have:**
```cmd
python -c "import pandas as pd; print(pd.read_csv('data\input\your_file.csv').columns.tolist())"
```
Then use `--text-column` with the right name!

---

## 🎓 Pro Tips for PhD Survival

1. **Start small** - Test with 10-20 papers first
2. **Name your files clearly** - Future you will appreciate it
3. **Always check a few results** - Make sure the AI isn't hallucinating species
4. **Use the species summary** - Great for finding research gaps and trends
5. **Keep your results organized** - Copy output files somewhere safe

---

## 🎪 The Complete Cheat Sheet

```cmd
# The daily routine:
cd C:\Users\YourName\Desktop\LitReview
venv\Scripts\activate
python scripts\extract_species.py data\input\your_file.csv

# Check what files you have:
dir data\input

# If your text column is called something else:
python scripts\extract_species.py data\input\your_file.csv --text-column summary
```

---

## 🎉 You're Now a Species-Extraction Wizard!

Drop your literature CSVs into `data\input\`, run the magic command, and let the AI do what it does best - finding all those "*Ursus maritimus*" and "*Escherichia coli*" mentions so you don't have to!

Now go forth and organize that literature like the academic rockstar you are! 🤘📚✨

*P.S. - When your advisor asks how you found all these species patterns so quickly, just smile mysteriously and say "I have my methods..." 😉*