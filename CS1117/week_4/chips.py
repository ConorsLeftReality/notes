number_of_bags                  = int(input("Number of bags >>> "))
number_of_chips_per_bag         = int(input("Number of chips per bag >>> "))

bags_consumed = 0
for bags_consumed in range(0,number_of_bags):
    chips_consumed = 0
    for chips_consumed in range(0,number_of_chips_per_bag):
        print("Nom Nom Nom, nice chip")
        chips_consumed += 1
    print("BAG DONE")
    bags_consumed += 1