class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"
    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print("""Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics""")

    def add(self, args):
        args[0] = int(args[0])
        cp = args[0]
        while cp in self.current_items.keys():
            self.current_items[-cp] = self.current_items.pop(cp)
            cp += 1
        self.current_items[args[0]] = args[0]
        keys = list(self.current_items.keys())
        for i in keys:
            if i < 0:
                self.current_items[-i + 1] = self.current_items.pop(i)
        self.current_items[int(args[0])] = args[1]
        self.write_current()
        print(f'Added task: "{args[1]}" with priority {args[0]}')

    def done(self, args):
        task = self.delete(args)
        if task:
            print("Marked item as done.")
            self.completed_items.append(task)
            self.write_completed()
        else:
            print(f"Error: no incomplete item with priority {args[0]} exists.")
            
    def delete(self, args):
        if int(args[0]) in self.current_items.keys():
            task = self.current_items.pop(int(args[0]))
            print(f"Deleted item with priority {args[0]}")
            self.write_current()
            return task
        else:
            print(f"Error: item with priority {args[0]} does not exist. Nothing deleted.")

    def ls(self):
        num = 1
        for key in sorted(self.current_items.keys()):
            print(f"{num}. {self.current_items[key]} [{key}]"); num += 1

    def report(self):
        print("Pending :", len(self.current_items))
        self.ls()
        print("\nCompleted :", len(self.completed_items))
        for i in range(len(self.completed_items)):
            print(f"{i+1}. {self.completed_items[i]}")
