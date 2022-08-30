# MySQL

## Instalação do MySQL no Ubuntu

```
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```
Após inserir uma senha pode aparecer a seguinte mensagem
```
... Failed! Error: SET PASSWORD has no significance for user 'root'@'localhost' as the authentication method used doesn't store authentication data in the MySQL server. Please consider using ALTER USER instead if you want to change authentication parameters.
```
Caso isso ocorra encerre o processo e insira
```
sudo mysql
```
Em seguida insira
```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'mynewpassword';
\q
```
Trocando mynewpassword pela sua senha. De novamente o comando
```
sudo mysql_secure_installation
``` 
Após isso é possível continuar a instalação normalmente. Agora para acessar o mysql 
```
sudo mysql -u root -p
```
e inserir a senha.