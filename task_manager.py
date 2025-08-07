from pathlib import Path


import re
import datetime

class TaskManager:
    def __init__(self, filename="data.txt"):
        self.filename = filename

    def create_backup(self):
        import shutil
        backup_file = self.filename.replace(".txt", "_backup.txt")
        shutil.copy(self.filename, backup_file)
        print(f"📁 Backup created as: {backup_file}")

    def add_task(self):
        print("==== Welcome to Task Manager ====")
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        while True:
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(deadline, "%Y-%m-%d")
                break
            except ValueError:
                print("❌ Invalid date format. Try again.")
        while True:
            priority = input("Enter priority (High/Medium/Low): ").capitalize()
            if priority in ["High", "Medium", "Low"]:
                break
            else:
                print("❌ Invalid priority. Choose High, Medium, or Low.")
        category = input("Enter category: ").strip()
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                
                f.write(f"Title:{title}\n")
                f.write(f"Description:{description}\n")
                f.write(f"Deadline:{deadline}\n")
                f.write(f"Priority:{priority}\n")
                f.write(f"Category:{category}\n")
                f.write("==========================\n")
        except Exception as e:
            print(f"Error saving task: {e}")

    def search_task(self, field):
      try:
          with open(self.filename, "r", encoding="utf-8") as f:
              lines = f.readlines()
      except FileNotFoundError:
          print("No file found")
          return

      value = input(f"Enter the {field.lower()} to search task: ").strip()
      pattern = rf"^{re.escape(field)}:\s*{re.escape(value)}$"
      found = False
      block = []

      for line in lines:
          if line.strip() == "==========================":
              # Check current block before resetting
              if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
                  print("\n".join(block))
                  print("========================")
                  found = True
              block = []
          else:
              block.append(line.strip())

    # ✅ Also check last block if file doesn't end with ========================
      if block:
          if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
              print("\n".join(block))
              print("========================")
              found = True

      if not found:
          print(f"No contact found with that {field.lower()}.")


    def delete_task(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("⚠️ No file found")
            return
        value = input("Enter title to delete task: ").strip()
        pattern = rf"^Title:\s*{re.escape(value)}"
        new_lines, block = [], []
        found_any = False

        for line in lines:
            if line.strip() == "==========================":
                if any(re.search(pattern, l, re.IGNORECASE) for l in block):
                    print("\n🔍 Matched Task Record:")
                    print("".join(block))
                    confirm = input("Do you want to delete this task? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        self.create_backup()
                        found_any = True
                        # skip
                    else:
                        new_lines.extend(block + ["==========================\n"])
                else:
                    new_lines.extend(block + ["==========================\n"])
                block = []
            else:
                block.append(line)

        if found_any:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("✅ Selected task(s) deleted.")
        else:
            print("❌ No task found with that title.")

    def update_task(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("⚠️ No file found")
            return
        value = input("Enter title to update task: ").strip()
        pattern = rf"^Title:\s*{re.escape(value)}"
        new_lines, block = [], []
        found_any = False

        for line in lines:
            if line.strip() == "==========================":
                if any(re.search(pattern, l, re.IGNORECASE) for l in block):
                    print("\n🔍 Matched Task Record:")
                    print("".join(block))
                    confirm = input("Do you want to update this task? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        self.create_backup()
                        found_any = True
                        new_title = input("Enter new title: ")
                        new_description = input("Enter new description: ")
                        while True:
                            new_deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
                            try:
                                datetime.datetime.strptime(new_deadline, "%Y-%m-%d")
                                break
                            except ValueError:
                                print("❌ Invalid date format.")
                        while True:
                            new_priority = input("Enter priority (High/Medium/Low): ").capitalize()
                            if new_priority in ["High", "Medium", "Low"]:
                                break
                            else:
                                print("❌ Invalid priority.")
                        new_category = input("Enter category: ")
                        
                        new_lines.append(f"Title:{new_title}\n")
                        new_lines.append(f"Description:{new_description}\n")
                        new_lines.append(f"Deadline:{new_deadline}\n")
                        new_lines.append(f"Priority:{new_priority}\n")
                        new_lines.append(f"Category:{new_category}\n")
                        new_lines.append("==========================\n")
                    else:
                        new_lines.extend(block + ["==========================\n"])
                else:
                    new_lines.extend(block + ["==========================\n"])
                block = []
            else:
                block.append(line)

        if found_any:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("✅ Task(s) updated successfully.")
        else:
            print("❌ No matching task found.")

    def list_titles(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("⚠️ No file found")
            return
        titles = [line.strip().replace("Title:", "") for line in lines if line.startswith("Title:")]
        if titles:
            print("📋 All Titles:")
            for idx, title in enumerate(titles, 1):
                print(f"{idx}. {title}")
        else:
            print("No titles found.")

    def print_all_tasks(self):
      try:
          with open(self.filename, "r", encoding="utf-8") as f:
              lines = f.readlines()
      except FileNotFoundError:
          print("⚠️ No file found")
          return

      block = []
      task_num = 1
      found = False

      for line in lines:
          if line.strip() == "==========================":
              if block:
                  print(f"\nTask {task_num}:")
                  print("".join(block).strip())
                  task_num += 1
                  found = True
              block = []
          else:
              block.append(line)

      if not found:
          print("No task found.")


if __name__ == "__main__":
    obj = TaskManager()
    while True:
        print("\n===== Task Manager Menu =====")
        print("1. Add Task")
        print("2. Search Task")
        print("3. Delete Task ")
        print("4. Update Task ")
        print("5. List All Titles")
        print("6. Print All Tasks")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            obj.add_task()
        elif choice == "2":
            print("Make sure write (Title//Category) otherwise it does not work")
            print()
            field = input("Search by (Title//Category): ").strip().capitalize()
            obj.search_task(field)
        elif choice == "3":
            obj.delete_task()
        elif choice == "4":
            obj.update_task()
        elif choice == "5":
            obj.list_titles()
        elif choice == "6":
            obj.print_all_tasks()
        elif choice == "7":
            print("👋 Exiting Task Manager. Goodbye!")
            break
        else:
            print("❌ Invalid input. Try again.")

