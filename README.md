# fair_ethereum_smart_contract_lottery

Project: Learning ethereum smart contract and blockchain technology

To test this project follow the instructions below:  

1. Download project and open ethereum_smart_contract_lottery/lottery/views.py file to change every appearance of  
   '/home/djordje/ethereum_smart_contract_lottery/lottery/smart_contract.sol' to full path of   
   .../ethereum_smart_contract_lottery/lottery/smart_contract.sol file on your computer.

2. Download Ganache software from https://www.trufflesuite.com/ganache and set local blockchain on address HTTP://127.0.0.1:7545.

3. Open https://remix.ethereum.org/ site and load smart_contract.sol file, connect you ganache blockchain and deploy smart contract at an address.
   For example my address is 0xb6eF88560d255bA8766462F161f415160613FC02 and you have to change every appearence of this address
   to address of your deployed smart contract in ethereum_smart_contract_lottery/lottery/views.py file.
 
4. Go to project directory: cd fair_ethereum_smart_contract_lottery/ethereum_smart_contract_lottery

5. Run django server: python manage.py runserver

6. Go to http://localhost:8000/lottery to open lottery web application 


