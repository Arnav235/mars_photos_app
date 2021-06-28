scores_arr = []
with open('./image_scores.txt') as file:
	lines_arr = [line.strip('\n') for line in file]
	for line in range(0, len(lines_arr), 2):
		arr = [float( lines_arr[line].strip().replace('Popularity score: ', '') ), lines_arr[line+1]]
		scores_arr.append(arr)

scores_arr.sort()
for list in scores_arr:
	print (list[0], " " + list[1])