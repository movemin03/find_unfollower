import os
import zipfile
import shutil
import json

def extract_and_move_json_files(zip_path, destination_folder):
    # Zip 파일이 존재하는지 확인
    if not os.path.isfile(zip_path):
        print(f"{zip_path} does not exist.")
        return None, None

    # 지정된 경로에 폴더가 있는지 확인하고 없으면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    followers_file = None
    following_file = None

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # zip 파일 내의 'followers_and_following' 폴더를 찾기
        for file_info in zip_ref.infolist():
            # 파일명이 "followers_1.json"이거나 "following.json"인 경우에만 처리
            if file_info.filename == 'followers_and_following/followers_1.json':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                followers_file = destination
                print(f"Copied: {file_info.filename} to {destination}")

            if file_info.filename == 'followers_and_following/following.json':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                following_file = destination
                print(f"Copied: {file_info.filename} to {destination}")

    return followers_file, following_file


desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
print("Find your Unfollower\n")
print("Before Use this program, pleas download your date from official instagram")
print("***You have to download json files not html****")
print("***You don't have to extract your file. Just input zip file\n")
zip_file_path = input("Enter the path to the zip file: ").replace('"', "")

# 함수를 호출하여 작업을 실행하고 결과를 변수에 저장
followers_file, following_file = extract_and_move_json_files(zip_file_path, desktop)

if followers_file is None or following_file is None:
    print("Failed to extract and move JSON files.")
else:
    print("followers_file:", followers_file)
    print("following_file:", following_file)

# 파일에서 데이터 로드
with open(followers_file, "r", encoding="utf-8") as f:
    followers_data = json.load(f)

with open(following_file, "r", encoding="utf-8") as f:
    following_data = json.load(f)

# 필요한 데이터 추출
followers_list = [follower["string_list_data"][0]["value"] for follower in followers_data]
following_list = [following["string_list_data"][0]["value"] for following in following_data["relationships_following"]]

# 팔로잉 목록에는 있지만 팔로워 목록에는 없는 값을 추려내기
unfollowers = [user for user in following_list if user not in followers_list]

# 결과를 unfollowers.txt 파일로 저장
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # 바탕화면 경로
unfollowers_file = os.path.join(desktop_path, "unfollowers.txt")  # 저장할 파일 경로

with open(unfollowers_file, "w", encoding="utf-8") as f:
    for user in unfollowers:
        f.write(user + "\n")

print(f"We save Unfollowers list to desktop/unfollowers.txt")
print(f"언팔로우 한 사람들의 리스트를 바탕화면에 unfollowers.txt 이름으로 저장했습니다")
