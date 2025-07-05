import re
import datetime
class Task_Manager:
  def __init__(self,filename="data.txt"):
    self.filename=filename 
  def add_task(self):
    print("====Welcome to task manager====")
    title=input("Enter title: ")
    description=input("Enter description: ")
    while True:
      deadlinedate=input("Enter deadline date(YYYY-MM-DD): ")
      try:
        datetime.datetime.strptime(deadlinedate, "%Y-%m-%d")
        break 
      except ValueError:
        print("❌ Invalid date format. Try again.")
    while True:
      priority=input("Enter priority(High/Medium/Low): ").capitalize()
      if priority in["High","Medium","Low"]:
        break
      else:
        print("❌ Invalid priority. Please choose High, Medium, or Low.")
    category=input("Enter category: ")
    try:
      with open(self.filename,"a") as f:
        f.write("==========================\n")
        f.write(f"Title:{title}\n")
        f.write(f"Description:{description}\n")
        f.write(f"Deadline:{deadlinedate}\n")
        f.write(f"Priority:{priority}\n")
        f.write(f"Category:{category}\n")
        f.write("==========================\n")
    except Exception as e:
      print(f"Error saving task:{e}")
  def search_by_title(self):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    title=input("Enter the title: ")
    pattern = rf"^Title:\s*{re.escape(title)}"
    found=False
    for i,line in enumerate(lines):
      if re.search(pattern,line,re.IGNORECASE):
        for j in range(i-1,i+7):
          if 0<=j<len(lines):
            print(lines[j].strip())
        found=True 
        break 
    if not found:
      print("No task found with that title")
  def search_by_category(self):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return 
    category=input("Enter category: ")
    pattern = rf"^Category:\s*{re.escape(category)}"
    found=False
    for i,line in enumerate(lines):
      if re.search(pattern,line,re.IGNORECASE):
        for j in range(i-1,i+7):
          if 0<=j<len(lines):
            print(lines[j].strip())
        found=True 
        break 
    if not found:
      print("No task found for that category")
  def search_by_deadlinedate(self):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found ")
      return 
    while True:
      deadlinedate=input("Enter the date: ")
      try:
        datetime.datetime.strptime(deadlinedate, "%Y-%m-%d")
        break 
      except ValueError:
        print("❌ Invalid date format. Try again.")
    pattern = rf"^Deadline:\s*{re.escape(deadlinedate)}" 
    found=False 
    for i,line in enumerate(lines):
      if re.search(pattern,line,re.IGNORECASE):
        for j in range(i-1,i+7):
          if 0<=j<len(lines):
            print(lines[j].strip())
        found=True
        break 
    if not found:
      print("NO file found")
  def delete_task_by_title(self):
    title=input("Enter title: ")
    new_lines=[]
    pattern = rf"^Title:\s*{re.escape(title)}"
    found=False 
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    i=0
    while i<len(lines):
      line=lines[i]
      if re.search(pattern,line,re.IGNORECASE):
        found=True
        while i>0 and lines[i-1].startswith("="):
          i-=1 
        while i<len(lines) and not lines[i].startswith("="):
          i+=1 
        if i<len(lines):
          i+=1 
      else:
        new_lines.append(line)
        i+=1 
    if found:
      with open(self.filename,"w") as f:
        f.write("".join(new_lines))
      print("Task deleted successfully")
    else:
      print("No task found with that title")
  def update_task_by_title(self):
    title=input("Enter the title: ")
    pattern = rf"^Title:\s*{re.escape(title)}"
    found=False
    new_lines=[]
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    i=0
    while i < len(lines):
      line=lines[i]
      if re.search(pattern,line,re.IGNORECASE):
        found=True 
        while i > 0 and not lines[i-1].startswith("=========================="):
          i-=1 
        while i < len(lines) and not lines[i].startswith("=========================="):
          i+=1 
        if i < len(lines):
          i+=1 
        
        new_title=input("Enter the title: ")
        new_description=input("Enter the description: ")
        while True:
          new_deadlinedate=input("Enter the deadline: ")
          try:
            datetime.datetime.strptime(new_deadlinedate, "%Y-%m-%d")
            break
          except ValueError:
            print("❌ Invalid date format. Try again.")
        new_category=input("Enter the category: ")
        while True:
          new_priority=input("Enter the priority(High/Medium/Low): ")
          if new_priority in["High","Medium","Low"]:
            break 
          else:
            print("❌ Invalid priority. Please choose High, Medium, or Low.")
        new_lines.append("==========================\n")
        new_lines.append(f"Title:{new_title}\n")
        new_lines.append(f"Description:{new_description}\n")
        new_lines.append(f"Deadline:{new_deadlinedate}\n")
        new_lines.append(f"Priority:{new_priority}\n")
        new_lines.append(f"Category:{new_category}\n")
        new_lines.append("==========================\n")

      else:
        new_lines.append(line)
        i+=1
    if found:
      with open(self.filename,"w") as f:
        f.write("".join(new_lines))
      print("Task updated successfully")
    else:
      print("No file found")
  def list_all_titles(self):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    titles=[line.strip().replace("Title:","") for line in lines if line.startswith("Title:")]
    if titles:
      print("----All saved Titles----\n")
      for idx,title in enumerate(titles,1):
        print([idx],[title])
      print("-------------------\n")
    else:
      print("No task found")
  def print_all_tasks(self):
    try:
      with open(self.filename,"r") as f:
        content=f.read().strip()
        print("\n --------All Saved Task-------- \n")
        parts=re.findall(r"=+\n(.*?)\n=+", content, re.DOTALL) 
        if parts: 
          for i,part in enumerate(parts,1):
              print(f"Task{i}")
              print(part.strip())
              print()
        else:
          print("No task found")
    except FileNotFoundError:
      print("No file found")
if __name__ == "__main__":
  obj=Task_Manager()
  while True:
    menu=input("Enter what you want to do\n1.add_task\n2.search_by_title\n3.search_by_category\n4.search_by_deadlinedate\n5.delete_task_by_title\n6.update_task_by_title\n7.list_all_titles\n8.print_all_tasks\n(1/2/3/4/5/6/7/8) or 'q' to quit: ")
    
    if menu == "1":
      obj.add_task()
    elif menu == "2":
      obj.search_by_title()
    elif menu == "3":
      obj.search_by_category()
    elif menu == "4":
      obj.search_by_deadlinedate()
    elif menu == "5":
      obj.delete_task_by_title()
    elif menu == "6":
      obj.update_task_by_title()
    elif menu == "7":
      obj.list_all_titles()
    elif menu == "8":
      obj.print_all_tasks()
    elif menu.lower() == "q":
      break