fibonacci_sayilari = [0, 1]

for i in range(2, 10):
    yeni_sayi = fibonacci_sayilari[-1] + fibonacci_sayilari[-2]
    fibonacci_sayilari.append(yeni_sayi)

print("Fibonacci Dizisi (ilk 10 sayı):", fibonacci_sayilari)