
![Header Image](https://preview.ibb.co/cxO2Qd/header.png)

# Bitcoin Blk Parser

This tool is a parser for the blk files of the Bitcoin blockchain. You can use it to parse raw hexadecimal blocks into json, it also contains a really simple blockchain explorer. After parsing data into json you will need to run a second script in order to get the sender address of transactions.

![Demo : raw data to json](https://preview.ibb.co/fapvBJ/demo.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* You need to install Python 3 on your computer.
```
> sudo apt-get install python3.X
```
* The readdressing script needs pySpark to run. You can find a good tutorial to install pySpark [HERE](https://www.tutorialspoint.com/pyspark/pyspark_environment_setup.htm)

### Installing

Download or clone this repo
```
> git clone https://github.com/PilouInfo/blk_parser.git
```

## Using Blk_Parser

### Blk_Parser

Blk_Parser has two different modes : fast parsing, and Cli.
* The fast parsing mode converts raw blk files into json files
	* `-i` : path to the input folder (blk .dat files)
	* `-o` : path to the output folder (json files)
	* `-n` : id (number) of the blk file to parse, use `*` to parse every blk files in the input folder
```
$> cd script
$> python3 blk_parser.py -i ./../data -o ./../result -n *
```
* The Cli mode let you parse and explore blk files
	* `-c` : run blk_parser in Cli mode
```
$> cd script
$> python3 blk_parser.py -c
blk_parser> help 
```
* To display the help message run the script with `-h` option
```
$> cd script
$> python3 blk_parser.py -h
```


### Readdressing
After parsing data into json you might have noticed that some transactions doesn't contain the sender address, this is because these addresses are stored elsewhere in the blockchain as receiver addresses. So you need to run the readdressing script in order to complete the missing sender addresses. Due to the massive amount of data to process the readdressing script run with the help of Apache Spark.
* `-i` : the folder containing the json files to readdress
* `-o` : the folder where the readdressed files will be stored
* `-h` : display the help message
```
$> cd script
$> spark-submit readdress.py -i ./../result -o ./../readdressed
```
**/!\ Warning /!\\**
If the output folder already exists on your computer, it will be deleted along with all its content ! Be sure to move or rename this folder (if it exist) before running the readdressing script.

## Author

* **Pierre-Louis DESPAIGNE**

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE.txt](LICENSE.txt) file for details

