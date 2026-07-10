### First Question

![[Pasted image 20260503175058.png]]

First way - Octal Notation:
	Owner =>  Read , Write , Execute     `rwx` = `7`
	Group =>  Read ,  Execute     `r-x` =  `5`
	Others => Execute only     `--x` = `1`

```bash
chmod 751 ~/myteam
```

Second Way -  Symbolic Notation:
```bash
chmod u=rwx,g=rx,o=x ~/myteam
```

Third Way - Symbolic Notation
```bash
chmod u+rwx,g-w+rx,o-rw+x ~/myteam
```

---
### Second Question

![[Pasted image 20260503180936.png]]
![[Pasted image 20260503181011.png]]

The text where it extracted 4 emails from: 
```text
This is a sample text file to test the email extraction script. Here are some valid email addresses mixed in: Please contact support at support@example.com for assistance. You can also reach out to the admin: admin.user123@company.co.uk. Another valid format is first-last_name@my-domain.org. Now, let's add some tricky or invalid formats that the script should ignore: This is missing a domain: user@domain This is missing the extension: user@domain. This has no user part: @example.com Just a website, not an email: www.google.com or http://test.com And here is one more valid email hidden at the end of a sentence: hello.world+test@sub.domain.net!
```

---
### Third Question 
![[Pasted image 20260503181231.png]]

`>` to create the file 
`>>` to append 

Combine three commands using pipes to display the number of files in your home directory in both the terminal and file.txt:

list -> ls
count -> wc
output -> tee

```bash 
ls ~ | wc -l | tee file.txt
```