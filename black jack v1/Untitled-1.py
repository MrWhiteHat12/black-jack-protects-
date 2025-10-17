lists = int(input("How many lists do you want? "))
varname = 'list'
for i in range(lists):
    exec(f"{varname}{i} = []")
print(list1)
exec(f'print(f"list{lists-1} is", list{lists-1})')
