



def tambah(x, y):
    return x + y

def kurang(x, y):
    return x - y

def kali(x, y):
    return x * y

def menu():
    print("Pilih Operasi.")
    print("1. Tambah")
    print("2. Kurang")
    print("3. Kali")
    print("4. Keluar")
    
while True:
    menu()
    pilihan = input("Masukkan pilihan (1/2/3/4): ")
    if pilihan in ('1', '2', '3'):
        num1 = float(input("Masukkan bilangan pertama: "))
        num2 = float(input("Masukkan bilangan kedua: "))
        if pilihan == '1':
            print("Hasil: ", tambah(num1, num2))
        elif pilihan == '2':
            print("Hasil: ", kurang(num1, num2))
        elif pilihan == '3':
            print("Hasil: ", kali(num1, num2))
    elif pilihan == '4':
        break
    else:
        print("Input tidak valid")
        
