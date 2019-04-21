my_file = open("all_pairs_2.txt", "r")
data = my_file.readlines()
my_file.close()

new_file = open("all_pairs_2.txt", "w")

for i in range(len(data)):
	if (len(data[i].split())) > 0:
		if (data[i].split()[0] != '<br><br>>' and data[i].split()[1] != '<br><br>>'):
			new_file.write(data[i].split()[0])
			new_file.write(' ')
			new_file.write(data[i].split()[1])
			new_file.write(' ')
			new_file.write(data[i].split()[2])
			new_file.write('\n')

new_file.close()
