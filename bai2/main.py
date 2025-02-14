
def read_player_data_from_txt(file_path):
    players = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # Bỏ qua dòng tiêu đề
        header = file.readline().strip().split("\t")

        # Đọc từng dòng dữ liệu
        for line in file:
            # Tách các giá trị bằng dấu tab và thêm vào danh sách
            values = line.strip().split("\t")
            players.append(values)
    return players

# Sử dụng hàm để đọc dữ liệu cầu thủ từ file player_data.txt
player_data = read_player_data_from_txt('E:/World/Code/Python/BTL/bai1/file/player_data.txt')
squad_data = read_player_data_from_txt('E:/World/Code/Python/BTL/bai1/file/squad_data.txt')

from tieu_de import header
from max_min_player import *

list_mm = max_min()

for index, value in enumerate(header):
    if index < 3: continue
    player_data = sorted(player_data, key=lambda x: x[index])
    list_mm.add_max_min([value, player_data[0][0], player_data[1][0], player_data[2][0], player_data[-3][0],player_data[-2][0], player_data[-1][0]])

# import openpyxl
#
# # Lưu dữ liệu vào file Excel cho player_manager
# wb = openpyxl.Workbook()
# ws = wb.active
# ws.title = "Players"
#
# # Ghi tiêu đề (header)
# ws.append(header_max_min)
#
# # Ghi dữ liệu của các cầu thủ
# for player in list_mm.list_max_min:
#     ws.append(player)
#
# # Lưu vào file Excel
# wb.save('E:/World/Code/Python/BTL/bai2/file/result.xlsx')
# print("Exam 1 Success - Player Data Saved")


import statistics

def calculate_median_for_player_data(player_data):
    # Giả sử mỗi phần tử của player_data chứa danh sách các giá trị [name, team, ..., chỉ số 1, chỉ số 2,...]
    # Tạo các danh sách rỗng cho các chỉ số
    num_columns = len(player_data[0])  # Số cột dữ liệu
    columns = [[] for _ in range(num_columns)]

    # Trích xuất dữ liệu các chỉ số (bỏ qua cột tên và đội nếu cần)
    for row in player_data:
        for i in range(len(row)):
            try:
                # Chuyển dữ liệu thành float (bỏ qua các cột không phải số nếu cần)
                value = float(row[i])
                columns[i].append(value)
            except ValueError:
                continue  # Bỏ qua các giá trị không phải số

    # Tính trung vị cho mỗi cột chỉ số
    medians = []
    for col in columns:
        if len(col) > 0:  # Đảm bảo cột không rỗng
            medians.append(statistics.median(col))
        else:
            medians.append(None)  # Nếu cột không có giá trị nào

    return medians

player_medians = calculate_median_for_player_data(player_data)
print("Player Medians:", player_medians)



def calculate_mean_std_for_player_data(player_data):
    # Giả sử mỗi phần tử của player_data chứa danh sách các giá trị [name, team, ..., chỉ số 1, chỉ số 2,...]
    num_columns = len(player_data[0])  # Số cột dữ liệu
    columns = [[] for _ in range(num_columns)]

    # Trích xuất dữ liệu các chỉ số (bỏ qua cột tên và đội nếu cần)
    for row in player_data:
        for i in range(len(row)):
            try:
                # Chuyển dữ liệu thành float (bỏ qua các cột không phải số)
                value = float(row[i])
                columns[i].append(value)
            except ValueError:
                continue  # Bỏ qua các giá trị không phải số

    # Tính trung bình và độ lệch chuẩn cho mỗi cột chỉ số
    stats = []
    for col in columns:
        if len(col) > 1:  # Đảm bảo cột có nhiều hơn 1 giá trị để tính độ lệch chuẩn
            mean = statistics.mean(col)
            std_dev = statistics.stdev(col)
            stats.append((mean, std_dev))
        else:
            stats.append((None, None))  # Nếu cột không có giá trị hoặc quá ít

    return stats

player_stats = calculate_mean_std_for_player_data(player_data)

for idx, (mean, std_dev) in enumerate(player_stats):
    print(f"Chỉ số {idx}: Trung bình = {mean}, Độ lệch chuẩn = {std_dev}")





import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_and_save_each_stat(player_data, output_folder):
    num_columns = len(player_data[0])  # Số cột dữ liệu
    columns = [[] for _ in range(num_columns)]

    # Trích xuất dữ liệu các chỉ số (bỏ qua cột tên và đội)
    for row in player_data:
        for i in range(len(row)):
            try:
                # Chuyển dữ liệu thành float
                value = float(row[i])
                columns[i].append(value)
            except ValueError:
                continue  # Bỏ qua các giá trị không phải số

    # Tạo thư mục lưu các biểu đồ nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # Lưu từng biểu đồ dưới dạng ảnh riêng
    for idx, col in enumerate(columns):
        if len(col) > 1:  # Đảm bảo có dữ liệu
            plt.figure(figsize=(8, 6))
            sns.histplot(col, bins=20, kde=True)  # Histogram với đường cong KDE
            plt.title(f'Distribution of Stat {idx}')
            plt.xlabel(f'Stat {idx}')
            plt.ylabel('Frequency')
            plt.grid(True)
            output_path = os.path.join(output_folder, f'stat_{idx}.png')
            plt.savefig(output_path)  # Lưu từng biểu đồ dưới dạng file ảnh riêng
            plt.close()  # Đóng figure để giải phóng bộ nhớ

    print(f'All plots are saved in the folder: {output_folder}')

# Sử dụng hàm để vẽ và lưu từng biểu đồ vào các file riêng trong thư mục
plot_and_save_each_stat(player_data, 'player_stats')
plot_and_save_each_stat(squad_data, 'squad_data')
