from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import loader

import json
from web3 import Web3
from solcx import compile_source
from decimal import Decimal
from django.utils import timezone
import sys
import ast

from .forms import FormCreate, FormJoin


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def index(request):
    return render(request, 'lottery/index.html')


def createLottery(request):
    form = FormCreate()
    return render(request, 'lottery/createLottery.html', {'form': form})


def joinLottery(request):
    form = FormJoin()
    return render(request, 'lottery/joinLottery.html', {'form': form})
    
    
class LotteryGame():
    lottery_id = ''
    creator_address = ''
    lottery_status = ''
    
def listLotteries(request):
    list_of_lotteries = []
    
    ganache_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    compiled_contract = compile_source_file('/home/djordje/ethereum_smart_contract_lottery2/lottery/smart_contract.sol')
    contract_id, contract_interface = compiled_contract.popitem()
    gambling_contract = web3.eth.contract(address = '0xb6eF88560d255bA8766462F161f415160613FC02', abi = contract_interface['abi'])
    
    lastID = gambling_contract.functions.getLastID().call()
    for i in range(1, lastID+1):
        lottery_game = LotteryGame()
        lottery_game.lottery_id = str(i)
        lottery_game.creator_address = str(gambling_contract.functions.getCreatorAddress(i).call())
        lottery_game.lottery_status = str(gambling_contract.functions.getGameStatus(i).call())
        list_of_lotteries.append(lottery_game)
        
    return render(request, 'lottery/listLotteries.html', {'list_of_lotteries': list_of_lotteries})


def statusPage(request, status_id):
    return render(request, 'lottery/statusPage.html', {'status_id': status_id})
        

def create_form_handling(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormCreate(request.POST)
        status_id = 0
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ganache_url = "HTTP://127.0.0.1:7545"
            web3 = Web3(Web3.HTTPProvider(ganache_url))
            
            accountAddr = form.cleaned_data['account_address']
            if accountAddr[:2] != '0x':
                accountAddr = '0x'+accountAddr
            try:
                accountAddress = web3.toChecksumAddress(accountAddr)
                web3.eth.defaultAccount = accountAddress
            except:
                status_id = 1
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            compiled_contract = compile_source_file('/home/djordje/ethereum_smart_contract_lottery2/lottery/smart_contract.sol')
            contract_id, contract_interface = compiled_contract.popitem()
            
            gambling_contract = web3.eth.contract(address = '0xb6eF88560d255bA8766462F161f415160613FC02', abi = contract_interface['abi'])
            
            numOfParticipants = form.cleaned_data['num_of_participants']
            try:
                numOfParticipants = int(numOfParticipants)
                if (numOfParticipants < 2 and numOfParticipants > 1000):
                    status_id = 2
                    return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            except:
                status_id = 2
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            valueToInvest = form.cleaned_data['amount_to_invest']
            try:
                valueToInvest = float(valueToInvest)
            except:
                status_id = 3
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
            
            tx_hash2 = gambling_contract.functions.createGame(numOfParticipants).buildTransaction({'nonce':nonce, 'value':web3.toWei(Decimal(valueToInvest), 'ether')})
            
            private_key = form.cleaned_data['private_key']
            if private_key[:2] != '0x':
                private_key = '0x'+private_key
            try:
                signed_txn = web3.eth.account.sign_transaction(tx_hash2, private_key=private_key)
            except:
                status_id = 4
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            try:
                tx_hash3 = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            except:
                status_id = 11
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormCreate()

    return render(request, 'lottery/createLottery.html', {'form': form})


def join_form_handling(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormJoin(request.POST)
        status_id = 5
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ganache_url = "HTTP://127.0.0.1:7545"
            web3 = Web3(Web3.HTTPProvider(ganache_url))
            
            accountAddr = form.cleaned_data['account_address']
            if accountAddr[:2] != '0x':
                accountAddr = '0x'+accountAddr
            try:
                accountAddress = web3.toChecksumAddress(accountAddr)
                web3.eth.defaultAccount = accountAddress
            except:
                status_id = 1
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            compiled_contract = compile_source_file('/home/djordje/ethereum_smart_contract_lottery2/lottery/smart_contract.sol')
            contract_id, contract_interface = compiled_contract.popitem()
            
            lotteryID = form.cleaned_data['lottery_id']
            try:
                lotteryID = int(lotteryID)
            except:
                status_id = 7
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            gambling_contract = web3.eth.contract(address = '0xb6eF88560d255bA8766462F161f415160613FC02', abi = contract_interface['abi'])
            
            valueToInvest = form.cleaned_data['amount_to_invest']
            try:
                valueToInvest = float(valueToInvest)
            except:
                status_id = 3
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
            
            try:
                tx_hash2 = gambling_contract.functions.takeBet(lotteryID).buildTransaction({'nonce':nonce, 'value':web3.toWei(Decimal(valueToInvest), 'ether')})
            except:
                status_id = 10
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
                
            private_key = form.cleaned_data['private_key']
            if private_key[:2] != '0x':
                private_key = '0x'+private_key
            try:
                signed_txn = web3.eth.account.sign_transaction(tx_hash2, private_key=private_key)
            except:
                status_id = 4
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})
            
            try:
                tx_hash3 = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            except:
                status_id = 11
                return render(request, 'lottery/statusPage.html', {'status_id': status_id})

            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
    else:
        form = FormJoin()

    return render(request, 'lottery/joinLottery.html', {'form': form})


class LotteryDetails():
    lotteryID = ''
    creatorAddress = ''
    gameStatus = ''
    currentGameValue = ''
    amountToInvest = ''
    currentNumOfBets = ''
    gameCapacity = ''
    winnerIndex = ''
    winnerAddress = ''
    currentBets = []
    
class Bet():
    bet_index = ''
    invested_amount = ''
    gambler_address = ''
    bet_status = ''

def lotteryInfo(request, lottery_id):
    
    contractAddress = '0xb6eF88560d255bA8766462F161f415160613FC02'
    
    ganache_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    compiled_contract = compile_source_file('/home/djordje/ethereum_smart_contract_lottery2/lottery/smart_contract.sol')
    contract_id, contract_interface = compiled_contract.popitem()
    
    gambling_contract = web3.eth.contract(address = contractAddress, abi = contract_interface['abi'])
    
    lottery_id = int(lottery_id)
    lottery_details = LotteryDetails()
    lottery_details.lotteryID = str(lottery_id)
    lottery_details.creatorAddress = str(gambling_contract.functions.getCreatorAddress(lottery_id).call())
    lottery_details.gameStatus = str(gambling_contract.functions.getGameStatus(lottery_id).call())
    lottery_details.currentGameValue = str(web3.fromWei(int(gambling_contract.functions.getGameValue(lottery_id).call()), 'ether'))
    try:
        lottery_details.amountToInvest = str(web3.fromWei(int(gambling_contract.functions.getAmountToEnterGame(lottery_id).call()), 'ether'))
    except:
        lottery_details.amountToInvest = "Amount requested to participate no longer available."
    lottery_details.currentNumOfBets = str(gambling_contract.functions.getCurrentNumOfBets(lottery_id).call())
    lottery_details.gameCapacity = str(gambling_contract.functions.getGameCapacity(lottery_id).call())
    try:
        gameOutcomeArr = ast.literal_eval(str(gambling_contract.functions.getGameOutcome(lottery_id).call())) 
        lottery_details.winnerIndex = str(gameOutcomeArr[0])
        lottery_details.winnerAddress = str(gameOutcomeArr[1])
    except:
        lottery_details.winnerIndex = "You cannot view winner's index because game didn't complete yet!"
        lottery_details.winnerAddress = "You cannot view winner's address because game didn't complete yet!"
        
    currentGameBets = gambling_contract.functions.getCurrentGameBets(lottery_id).call()
    
    lottery_details.currentBets = []
    cntIndex = 0
    for b in currentGameBets:
        bet = Bet()
        bet.bet_index = str(cntIndex)
        cntIndex += 1
        bet.invested_amount = str(web3.fromWei(int(b[0]), 'ether'))
        bet.gambler_address = str(b[1])
        if str(b[2]) == "1":
            strStatus = 'Winner'
        if str(b[2]) == "2":
            strStatus = 'Loser'
        if str(b[2]) == "3":
            strStatus = 'Pending'
        bet.bet_status = strStatus
        lottery_details.currentBets.append(bet)
        
    return render(request, 'lottery/lotteryInfo.html', {'lottery_details': lottery_details})


class DataAndIndex():
    lottery_id = ''
    account_addr = ''
    index = ''

def checkIndex(request):
    if request.method == 'POST':
        your_address = request.POST['your_address']
        lottery_id = request.POST['lottery_id']
        
        ganache_url = "HTTP://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        
        if your_address[:2] != '0x':
            your_address = '0x'+your_address
        try:
            your_address = web3.toChecksumAddress(your_address)
            web3.eth.defaultAccount = your_address
        except:
            status_id = 12
            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
        
        try:
            contract_address = web3.toChecksumAddress('0xb6eF88560d255bA8766462F161f415160613FC02')
        except:
            status_id = 13
            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
        
        compiled_contract = compile_source_file('/home/djordje/ethereum_smart_contract_lottery2/lottery/smart_contract.sol')
        contract_id, contract_interface = compiled_contract.popitem()
        
        try:
            gambling_contract = web3.eth.contract(address = contract_address, abi = contract_interface['abi'])
        except:
            status_id = 14
            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
        
        lastID = int(gambling_contract.functions.getLastID().call())
        if not ((int(lottery_id) >= 1) and (int(lottery_id) <= lastID)):
            status_id = 7
            return render(request, 'lottery/statusPage.html', {'status_id': status_id})
        
        try:
            your_index = str(gambling_contract.functions.getMyIndex(int(lottery_id)).call())
        except:
            your_index = "You cannot have index as long as you are not a participant!"
        
        data_and_index = DataAndIndex()
        data_and_index.lottery_id = lottery_id
        data_and_index.account_addr = your_address
        data_and_index.index = your_index
        return render(request, 'lottery/checkIndex.html', {'data_and_index': data_and_index})
