User Creation
```linux
sudo adduser ahmed_elkassrawy #create account

id ahmed_elkassrawy #display id

su - ahmed_elkassrawy #switch to the user
```

![[Pasted image 20260302015600.png]]

Question 2:
Creating the files
![[Pasted image 20260302020120.png]]

```linux
cd ~ #the root/home folder

#created folders
mkdir -p ~/dir1/dir12/dir21 ~/dir1/dir13 ~/dir1/dir11/dir111 ~/docs 

#createe file
touch ~/dir1/dir13/myfile1 ~/dir1/dir11/myfile2 ~/docs/mycv
```

![[Pasted image 20260302020106.png]]

1. display hierarchy
```linux
tree ~ 
```

![[Pasted image 20260302020323.png]]

Copy file /etc/passwd to dir21
```linux
cp /etc/passwd ~/dir1/dir12/dir21/
```

Move myfile2 to dir13 
```linux
mv ~/dir1/dir11/myfile2 ~/dir1/dir13/
```

Remove dir11
```linux
rm -r ~/dir1/dir11
```

the hierarchy after the edits
```linux 
tree ~
```

![[Pasted image 20260302020710.png]]

my current directory : /home/ahmed_elkassrawy/dir1/dir12/dir21
path to mycv 
- Absolute Path
```linux
/home/ahmed_elkassrawy/docs/mycv
```

- Relative Path 
```linux
../../../docs/mycv
```
---
### Bonus Question
Creating folder for images: 
```linux
cd ~
mkdir images
```

creating new script file
```linux
nano split_dataset.sh
```

Script
```bash
#!/bin/bash

#define directory
SOURCE_DIR=~/images
DATASET_DIR=~/dataset

#createe target destination
mkdir -p "$DATASET_DIR"/train "$DATASET_DIR"/val "$DATASET_DIR"/test

#put files in array
files=("$SOURCE_DIR"/*)

#move 6 image to train
for i in {0..5}; do
	mv "${files[$i]}" "$DATASET_DIR/train/" 
done

move 2 images to val
for i in {6..7}; do 
	mv "${files[$i]}" "$DATASET_DIR/val/" 
done

#move 2 images to test
for i in {8..9}; do 
	mv "${files[$i]}" "$DATASET_DIR/test/" 
done

echo "Image successfuly spliited"
tree "$DATASET_DIR"

```

run the script
```bash
#executuble
chmod +x split_dataset.sh

#runing script
./split_dataset.sh
```