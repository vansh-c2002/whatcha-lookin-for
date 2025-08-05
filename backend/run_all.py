import subprocess

print("\n🚀 Starting full run...")

# Step 1: Web scraping and mp3 download
print("\n🌐 Running web scraping...")
subprocess.run(["python", "backend/webscraping.py"], check=True)

# Step 2: Stem separation + instrument detection
print("\n🧠 Running postprocessing...")
subprocess.run(["python", "backend/postprocess.py"], check=True)

print("\n✅ All done!")
