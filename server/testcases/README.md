# **CHAT SERVER TESTING**
## **Getting Started**
Please make sure you are in the *server* directory to correctly run the tests. Use the command *./mastertest.sh* to run the tests.\
Each test will start an instance of the *server.py* program in the background, using different ports for each set of tests.
The tests will start 2 or 3 different instances of the *client.py* program in the background, accepting input from a *.in* file and writing the output into it's corresponding *.out* file.
This output file will be compared to the expected *.exp* file.
If there is not difference between the files, the test is considered to have passed.\
Once all tests are completed for a certain function, *PASSED* or *FAILED* will be output.
If *PASSED* is output, all test cases have passed. If *FAILED* is output, one or more test cases have failed for that function. Details about which testcases have passed or failed can be found in *testing.json*.\
Please make sure you provide enough time between running the *./mastertest.sh* command as ports may still be occupied. If this is the case, the *server.py* program will output *PORT :PORTNUMBER IS STILL OPEN*. Please exit the test using `Ctrl + C` and wait until the port is unoccupied.

# **Test Case Inputs**
Below is a list of the inputs for each client in the tests and what each line aims to test.

## **Register Test**
This test uses port 2040.
### **Client 1**
| **Input Line**           | **Aim of test**                                    | **Expected Output** |
| ------------------------ | -------------------------------------------------- | ------------------- |
| REGISTER                 | Missing all arguments                              | RESULT REGISTER 0   |
| REGISTER user1           | Missing one argument                               | RESULT REGISTER 0   |
| REGISTER user1 password1 | Successful REGISTER                                | RESULT REGISTER 1   |
| REGISTER user1 password1 | Already registered user                            | RESULT REGISTER 0   |
| REGISTER user1 password2 | Already registered user (different password)       | RESULT REGISTER 0   |
| REGISTER USER1 password1 | Successful REGISTER with slightly changed username | RESULT REGISTER 1   |

### **Client 2**
| **Input Line**           | **Aim of test**                                      | **Expected Output** |
| ------------------------ | ---------------------------------------------------- | ------------------- |
| REGISTER user1 password1 | Already registered on other client                   | RESULT REGISTER 0   |
| REGISTER user2 password2 | Successful REGISTER on second client                 | RESULT REGISTER 1   |
| LOGIN user1 password1    | Successful LOGIN for user registered on other client | RESULT LOGIN 1      |

## **Login Test**
This test uses port 2050.
### **Client 1**
| **Input Line**           | **Aim of test**                     | **Expected Output** |
| ------------------------ | ----------------------------------- | ------------------- |
| REGISTER user1 password1 |                                     | RESULT REGISTER 1   |
| REGISTER user2 password2 |                                     | RESULT REGISTER 1   |
| LOGIN                    | Missing all arguments               | RESULT LOGIN 0      |
| LOGIN user1              | Missing one argument                | RESULT LOGIN 0      |
| LOGIN user1 password2    | Incorrect password                  | RESULT LOGIN 0      |
| LOGIN user1 password1    | Successful LOGIN                    | RESULT LOGIN 1      |
| LOGIN user2 password2    | Already logged into another account | RESULT LOGIN 0      |
| LOGIN user1 password1    | Account already logged on           | RESULT LOGIN 0      |

### **Client 2**
| **Input Line**        | **Aim of test**                                      | **Expected Output** |
| --------------------- | ---------------------------------------------------- | ------------------- |
| LOGIN user1 password1 | Already logged into user on other client             | RESULT LOGIN 0      |
| LOGIN user2 password2 | Successful LOGIN for user registered on other client | RESULT LOGIN 1      |

## **Create Test**
This test uses port 2060.
### **Client 1**
| **Input Line**           | **Aim of test**                                      | **Expected Output**                |
| ------------------------ | ---------------------------------------------------- | ---------------------------------- |
| REGISTER user1 password1 |                                                      | RESULT REGISTER 1                  |
| LOGIN user1 password1    |                                                      | RESULT LOGIN 1                     |
| CREATE                   | Missing all arguments                                | RESULT CREATE 0                    |
| CREATE channel1          | Successful CREATE                                    | RESULT CREATE channel1 1           |
| CREATE CHANNEL1          | Successful CREATE with slightly changed channel name | RESULT CREATE CHANNEL1 1           |
| CHANNELS                 | Channels created                                     | RESULT CHANNELS CHANNEL1, channel1 |

### **Client 2**
| **Input Line**           | **Aim of test**                    | **Expected Output**                          |
| ------------------------ | ---------------------------------- | -------------------------------------------- |
| CREATE channel2          | Not logged in                      | RESULT CREATE channel2 0                     |
| REGISTER user2 password2 |                                    | RESULT REGISTER 1                            |
| LOGIN user2 password2    |                                    | RESULT LOGIN 1                               |
| CREATE channel1          | Channel already created            | RESULT CREATE channel1 0                     |
| CREATE channel2          | Successful CREATE on second client | RESULT CREATE channel2 1                     |
| CHANNELS                 | Channels created from both clients | RESULT CHANNELS CHANNEL1, channel1, channel2 |

## **Join Test**
This test uses port 2070.
### **Client 1**
| **Input Line**           | **Aim of test**        | **Expected Output**   |
| ------------------------ | ---------------------- | --------------------- |
| REGISTER user1 password1 |                        | RESULT REGISTER 1     |
| LOGIN user1 password1    |                        | RESULT LOGIN 1        |
| CREATE alpha             |                        | RESULT CREATE alpha 1 |
| JOIN                     | Missing arguments      | RESULT JOIN 0         |
| JOIN bravo               | Channel does not exist | RESULT JOIN bravo 0   |
| JOIN alpha               | Successful JOIN        | RESULT JOIN alpha 0   |
| JOIN alpha               | Already joined channel | RESULT JOIN alpha 0   |

### **Client 2**
| **Input Line**           | **Aim of test**                    | **Expected Output** |
| ------------------------ | ---------------------------------- | ------------------- |
| JOIN alpha               | Not logged in                      | RESULT JOIN alpha 0 |
| REGISTER user2 password2 |                                    | RESULT REGISTER 1   |
| LOGIN user2 password2    |                                    | RESULT LOGIN 1      |
| JOIN alpha               | Successful JOIN from second client | RESULT JOIN alpha 1 |

## **Channels Test**
This test uses port 2080.
### **Client 1**
| **Input Line**           | **Aim of test**                      | **Expected Output**     |
| ------------------------ | ------------------------------------ | ----------------------- |
| REGISTER user1 password1 |                                      | RESULT REGISTER 1       |
| LOGIN user1 password1    |                                      | RESULT LOGIN 1          |
| CHANNELS                 | Successful CHANNELS but no channels  | RESULT CHANNELS         |
| CREATE charlie           |                                      | RESULT CREATE charlie 1 |
| CHANNELS                 | Successful CHANNELS with one channel | RESULT CHANNELS charlie |
| CREATE bravo             |                                      | RESULT CREATE bravo 1   |
| CREATE alpha             |                                      | RESULT CREATE alpha 1   |

### **Client 2**
| **Input Line** | **Aim of test**                                                                     | **Expected Output**                   |
| -------------- | ----------------------------------------------------------------------------------- | ------------------------------------- |
| CHANNELS       | Successful CHANNELS while not logged in and multiple channels in alphabetical order | RESULT CHANNELS alpha, bravo, charlie |

## **Say Test**
This test uses port 2090.
### **Client 1**
| **Input Line**           | **Aim of test**        | **Expected Output**   |
| ------------------------ | ---------------------- | --------------------- |
| REGISTER user1 password1 |                        | RESULT REGISTER 1     |
| LOGIN user1 password1    |                        | RESULT LOGIN 1        |
| SAY alpha hello there    | Channel does not exist | RESULT SAY 0          |
| CREATE alpha             |                        | RESULT CREATE alpha 1 |
| SAY alpha hello there    | Not joined channel     | RESULT SAY 0          |

### **Client 2**
| **Input Line**           | **Aim of test**                                              | **Expected Output**        |
| ------------------------ | ------------------------------------------------------------ | -------------------------- |
| SAY alpha g'day mate     | User not logged in                                           | RESULT SAY alpha 0         |
| REGISTER user2 password2 |                                                              | RESULT REGISTER 1          |
| LOGIN user2 password2    |                                                              | RESULT LOGIN 1             |
| JOIN alpha               |                                                              | RESULT JOIN alpha 1        |
|                          | Successful RECV message sent from client 3 to joined channel | RECV user3 alpha hey buddy |

### **Client 3**
| **Input Line**           | **Aim of test**          | **Expected Output**        |
| ------------------------ | ------------------------ | -------------------------- |
| REGISTER user3 password3 |                          | RESULT REGISTER 1          |
| LOGIN user3 password3    |                          | RESULT REGISTER 0          |
| JOIN alpha               |                          | RESULT JOIN alpha 1        |
| SAY bravo hey buddy      | Joined different channel | RESULT SAY bravo 0         |
| SAY alpha hey buddy      | Successful SAY           | RECV user3 alpha hey buddy |
| SAY alpha                | Missing argument         | RESULT SAY 0               |
| SAY                      | Missing all arguments    | RESULT SAY 0               |

## **Other Test**
This test uses port 3000. Unlike other tests there is no input into the program as it is expected to fail. This test is used to make sure the *server.py* program will output error messages when the port supplied is still open or no port number has been provided. The testing *server.py* calls are not made in the background to ensure that they exit upon outputting the error message.
| **Server call**  | **Aim of test**         | **Expected Output**          |
| ---------------- | ----------------------- | ---------------------------- |
| server.py 3000 & |                         |                              |
| server.py        | No port number provided | Please provide a port number |
| server.py 3000   | Port already occupied   | PORT 3000 IS STILL OPEN.     |