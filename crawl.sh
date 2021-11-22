declare -a arr=($(ls ./data/$1/))

for i in "${arr[@]}"
do
   if [ $i == "0.json" ] || [ $i == "1.json" ] || [ $i == "10.json" ] || [ $i == "11.json" ] 
   then
      echo "This is one!"
   else
      scrapy crawl info -a city=$1 -a index=$i -o "results/$1/$i" -t json
   fi
   # or do whatever with individual element of the array
   # scrapy crawl info -a city=$1 -a index=$i -o "results/$1/$i" -t json
done