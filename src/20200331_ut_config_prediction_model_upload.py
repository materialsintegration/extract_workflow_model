#!C:\\Python36\\python36.exe
# -*- coding: utf-8 -*-
# description:予測モデルIDをワークフローに設定する
# 要：
# 実行： python3.6.exe 20200331_ut_config_prediction_model_upload.py -o <chooselocation.mintsys.jp> -p <portNumber> -w <WorkFlowID> -t <MyToken>
# 想定環境：CentOS 7.4 x64 + python3.6

# imports section
import os
import sys
import argparse #process args
import subprocess #exec system commands
import time  #sleep 1s
import codecs #テキストファイルを文字エンコード指定して読む
import traceback #trace back 
import shutil #file copy
import glob #特定の拡張子を持つファイルを探させる
import re #正規表現ライブラリ
import requests #http処理用
import json #JSON可視化用
from collections import OrderedDict #順序保証付き辞書
import pprint # 辞書のダンプを見やすくする


# Class section
## アクセス情報クラス
class myAccessInfo:
    ## global
    
    ## vars
    
    mytoken = "<MyToken>" #MIntシステムユーザーのtoken
    target_host = "chooselocation.mintsys.jp" #MIntシステムのアクセス先
    myport = 443 #MIntシステムのWF-APIポート
    wf_api_ver = "v2" #WF-APIバージョン
    wf_api_name = "workflow-api" #WF-APIの名前（変わることあるのか？）
    inv_api_ver = "v5" #インベントリAPIのバージョン
    inv_api_name = "inventory-api" #インベントリAPIの名前（変わることあるのか？）
    inv_up_api_name = "inventory-update-api" #インベントリ更新API名（変わることはあるのか？）
    workflow_id = "" #ワークフローID、（円周率計算、錘付き）
    desc_id = "" #デスクリプターID、（円周率計算、桁数ファイル）
    
    ## static
    ### 東大運用のutrootが持っているトークン情報
    wfapi_headers={'Authorization': 'Bearer <MyToken>', 'Content-Type': 'application/json', 'Accept': 'application/json' }
    ### 東大運用環境のアクセス先、ワークフローは円周率計算を行うワークフローの錘ファイル対応版
    wfapi_acsuri = "https://chooselocation.mintsys.jp:443/workflow-api/v2/workflows/<WorkflowID>"
    invapi_acsuri = "https://chooselocation.mintsys.jp:443/inventory-api/v5/<DescriptorID>"
    inv_update_api_acsuri = "https://chooselocation.mintsys.jp:443/inventory-update-api/v5/prediction-models"
    wfupdate_api_acsuri = "https://chooselocation.mintsys.jp:443/workflow-api/v2/workflows"
    inv_predict_acsuri = "https://chooselocation.mintsys.jp:443/inventory/prediction-models/<PredictionModelID>"
    
    ## static
    
    ## インベントリ コンストラクタ
    ## コンストラクタ
    def __init__( self, target_host="chooselocation.mintsys.jp", myport=443, token="<MyToken>" , \
      wf_api_ver="v2", wf_api_name="workflow-api", inv_api_ver="v5", inv_api_name="inventory-api", inv_up_api_name="inventory-update-api",  \
      workflow_id="<WorkFlowID>", desc_id="<DescriptorID>" \
    ):
    
        ### 変数を設定する
        self.target_host = target_host
        self.myport = myport
        self.token = token
        self.wf_api_ver = wf_api_ver
        self.wf_api_name = wf_api_name
        self.inv_api_ver = inv_api_ver
        self.inv_api_name = inv_api_name
        self.inv_up_api_name = inv_up_api_name
        self.workflow_id = workflow_id
        self.desc_id = desc_id
        
        ### トークンの設定
        self.wfapi_headers["Authorization"] = "Bearer " + self.mytoken 
        ### make access infomations
        self.wfapi_acsuri = "https://" + self.target_host + ":" + str( self.myport ) + "/" + self.wf_api_name + "/" + self.wf_api_ver + "/workflows/" + self.workflow_id
        self.invapi_acsuri = "https://" + self.target_host + ":" + str( self.myport ) + "/" + self.inv_api_name + "/" + self.inv_api_ver + "/descriptors/" + self.desc_id
        self.inv_update_api_acsuri = "https://" + self.target_host + ":" + str( self.myport ) + "/" + self.inv_up_api_name + "/" + self.inv_api_ver + "/prediction-models"
        self.wfupdate_api_acsuri = "https://" + self.target_host + ":" + str( self.myport ) + "/" + self.wf_api_name + "/" + self.wf_api_ver + "/workflows/workflows"
        self.inv_predict_acsuri = "https://" + self.target_host + "/inventory/prediction-models/"
        
        if not __debug__:
            print( "WF-header: ")
            print( self.wfapi_headers )
            print( "WF-URI: " + self.wfapi_acsuri )
            print( "Inv-URI: " + self.invapi_acsuri )
            print( "Inv-up-URI: " + self.inv_update_api_acsuri )
            print( "WF-up-URI: " + self.wfupdate_api_acsuri )
            print( "PM-URI: " +  self.inv_predict_acsuri )
        
        
    ## メソッド群
    ### 
    #def  (self):
    #    pass
    
    
    ### 
    #def  (self):
    #    pass
    
    ### 
    #def (self):
    #    pass
    
    ### チェッカー関数
    
    ### toString()
    def __str__(self):

        tmpstr = "------myAccessInfo dump------" + os.linesep
        if self.target_host is not None:
            tmpstr += "host: " + self.target_host + os.linesep
        else :
            tmpstr += "host is not configure. " + os.linesep
        
        if self.myport is not None:
            tmpstr += "port: " + str( self.myport ) + os.linesep
        else:
            tmpstr += "port is not configure." + os.linesep
        
        if self.wf_api_ver is not None:
            tmpstr += "wf_api_ver: " + self.wf_api_ver + os.linesep
        else :
            tmpstr += "wf_api_ver is not configure." + os.linesep
        
        if self.wf_api_name is not None:
            tmpstr += "wf_api_name: " + self.wf_api_name + os.linesep
        else:
            tmpstr += "wf_api_name is not configure." + os.linesep
        
        if self.inv_api_ver is not None:
            tmpstr += "inv_api_ver: " + self.inv_api_ver + os.linesep
        else:
            tmpstr += "inv_api_ver is not configure." + os.linesep
        
        if self.inv_api_name is not None:
            tmpstr += "inv_api_name: " + self.inv_api_name + os.linesep
        else:
            tmpstr += "inv_api_name is not configure." + os.linesep
        
        if self.inv_up_api_name is not None:
            tmpstr += "inv_up_api_name: " + self.inv_up_api_name + os.linesep
        else:
            tmpstr += "inv_up_api_name is not configure." + os.linesep
        
        if self.workflow_id is not None:
            tmpstr += "workflow_id: " + self.workflow_id + os.linesep
        else:
            tmpstr += "workflow_id is not configure." + os.linesep
        
        if self.mytoken is not None:
            tmpstr += "token: " + self.mytoken + os.linesep
        else:
            tmpstr += "token is not configure." + os.linesep
        
        if self.wfapi_headers is not None:
            tmpstr += "WF-header: " + os.linesep + json.dumps(self.wfapi_headers, indent=2, ensure_ascii=False) + os.linesep
        else :
            tmpstr += "WF-header is not configure." + os.linesep
        
        if self.wfapi_acsuri is not None:
            tmpstr += "WF-URI: " + self.wfapi_acsuri + os.linesep
        else:
            tmpstr += "WF-URI is not configure." + os.linesep
        
        if self.wfupdate_api_acsuri is not None:
            tmpstr += "WF-UP-URI: " + self.wfupdate_api_acsuri + os.linesep
        else:
            tmpstr += "WF-UP-URI is not configure." + os.linesep
        
        if self.invapi_acsuri is not None:
            tmpstr += "INV-URI: " + self.invapi_acsuri + os.linesep
        else:
            tmpstr += "INV-URI is not configure." + os.linesep
        
        if self.inv_update_api_acsuri is not None:
            tmpstr += "INV-UP-URI: " + self.inv_update_api_acsuri + os.linesep
        else:
            tmpstr += "INV-UP-URI is not configure." + os.linesep
        
        tmpstr += "------End myAccessInfo dump------" + os.linesep
        
        ### 持っている変数情報をダンプ
        return tmpstr
        
    
    ### インベントリ デストラクタ
    def __del__(self):
    
        pass
    


## アップロードするインベントリのデータを作る
class myInventoryData:
    ## global
    
    ## vars
    lang = "ja" #日本語に設定する
    pd_name ="" #予測モデル名
    inputports = [] #入力ポート
    outputports = [] #出力ポート
    kindOfPred = "" #予測モデルの種類
    sofToolName = "" # ソフトウエアツール名
    pd_desc = "" #予測モデルの説明
    upload_json = "" #アップロードするJSONデータ
    pm_id = "" #予測モデルID
    pm_id_uri = "" #予測モデルIDのURI
    
    # CONST
    HTTP_OK = 200
    HTTP_OK2 = 201
    PRED_ID_LEN = -16 #予測モデルの長さ
    
    ## インベントリ コンストラクタ
    def __init__(self, acsinfo , myWorkFlowData ):
        
        self.acsinfo = acsinfo
        self.myWorkFlowData = myWorkFlowData
        
        self.inv_session=requests.Session() #インベントリAPIのセッションを開始
        
    ## メソッド群
    ### インベントリデータを取得する
    def getInventoryData(self):
    
        ### webアクセスしてインベントリデータを取ってくる
        self.invapi_ret=self.inv_session.get(self.acsinfo.invapi_acsuri, headers=self.acsinfo.wfapi_headers)
        if not __debug__:
            print("------inv-API------")
            print( "inv-API_res_code: " + str( self.invapi_ret.status_code ) )
            print(json.dumps(self.invapi_ret.json(), indent=2, ensure_ascii=False)) 
        
        if ( self.invapi_ret.status_code != self.HTTP_OK ) and ( self.invapi_ret.status_code != self.HTTP_OK2 ) :
            
            print("インベントリ情報の取得に失敗した" + os.linesep)
            raise OSError("Faild to got Inventory Description data." + os.linesep)
        
    
    
    ### 予測モデル情報を作る
    def mkPredictionModelData(self):
        self.pd_name = self.myWorkFlowData.wf_name
        self.pd_desc = self.myWorkFlowData.wf_description
        self.inputports = self.myWorkFlowData.inputport
        self.outputports = self.myWorkFlowData.outputport
        
        # JSONデータの構築
        tmp_json = {}
        tmp_json["preferred_name"] = self.pd_name
        tmp_json["preferred_name_language"] = self.lang
        tmp_json["description"] = self.pd_desc
        tmp_json["input_ports"] = self.inputports
        tmp_json["output_ports"] = self.outputports
        
        
        self.upload_json = json.dumps(tmp_json)
        print(json.dumps(tmp_json, indent=2, ensure_ascii=False)) 
    
    
    ### 予測モデル情報を送信する
    def upPredictionModelData(self):
        self.invapi_ret=self.inv_session.post(self.acsinfo.inv_update_api_acsuri, headers=self.acsinfo.wfapi_headers, data=self.upload_json)
        tmp_json = self.invapi_ret.json()
        print(json.dumps(tmp_json, indent=2, ensure_ascii=False)) 
        
        ### httpステータスを確認する
        if ( self.invapi_ret.status_code != self.HTTP_OK ) and ( self.invapi_ret.status_code != self.HTTP_OK2 ) :
        
            print( "インベントリ予測モデルの登録に失敗した。" + os.linesep )
            raise OSError(" Faild To update Inventory Prediction model " + os.linesep )
        
        tmpstr = tmp_json["prediction_model_id"]
        #print( "インベントリ予測モデルID: " + tmpstr + os.linesep)
        self.pm_id_uri = tmp_json["prediction_model_id"]
        self.pm_id = tmpstr[self.PRED_ID_LEN:]
        
        print("インベントリ予測モデルの登録に成功した( " + self.pm_id + " )" + os.linesep)
    
    
    ### 予測モデルIDを取得する
    def getPredictionModelID(self):
        return self.pm_id
    
    
    ### 予測モデルIDのURIを返す
    def getPredictionModelID_URI(self):
        return self.pm_id_uri
    
    ### チェッカー関数
    
    ### toString()
    def __str__(self):
    
        tmpstr = "------myInventoryData dump------" + os.linesep
        if self.acsinfo is not None:
            tmpstr += "INV_acs_uri: " + self.acsinfo.invapi_acsuri + os.linesep
        else :
            tmpstr += "INV_acs_uri is not defined." + os.linesep
        
        if self.invapi_ret is not None:
            tmpstr += "inv-API_res_code: " + str( self.invapi_ret.status_code ) + os.linesep
        else :
            tmpstr += "inv-API_res_code is not defined." + os.linesep
        
        if self.invapi_ret is not None:
            tmpstr += "INV_JSON-data: " + os.linesep + json.dumps(self.invapi_ret.json(), indent=2, ensure_ascii=False) + os.linesep
        else:
            tmpstr += "INV_JSON-data is not defined." + os.linesep
        
        if self.pm_id is not None:
            tmpstr += "PM_ID: " + self.pm_id + os.linesep
        else:
            tmpstr += "PM_ID is not defined." + os.linesep
        
        if self.pm_id_uri is not None:
            tmpstr += "PMD_ID_URI: " + self.pm_id_uri + os.linesep
        else:
            tmpstr += "PM_ID_URI is not defined." + os.linesep
        
        tmpstr += "------End myInventoryData dump------" + os.linesep
        ### インベントリ関係の情報をダンプ
        return tmpstr
        
    
    ### インベントリ デストラクタ
    def __del__(self):
    
        self.inv_session.close() #WF-APIのセッションを終了
    



## ワークフローデータを作る
class myWorkFlowData:
    ## global
    
    ## vars
    
    wf_update=-1 #リビジョン探索用
    sel_wf=0 #リビジョン探して選んだWF
    inputport=[] #入力ポート
    outputport=[] #出力ポート
    wf_name="" #ワークフロー名
    wf_description="" #ワークフローの説明
    pm_id="" #ワークフロー予測モデルID
    
    
    ## static
    HTTP_OK = 200
    HTTP_OK2 = 201
    PRED_ID_LEN = -16 #予測モデルの長さ
    
    ## コンストラクタ
    def __init__( self, acsinfo ):
    
        self.acsinfo = acsinfo
        self.wf_session=requests.Session() #WF-APIのセッションを開始
    
    ## メソッド群
    ### ワークフロー情報を取得する
    def getWorkflowData( self ):
    
        ### webにアクセスしてワークフロー情報を拾う
        self.wfapi_ret=self.wf_session.get(self.acsinfo.wfapi_acsuri, headers=self.acsinfo.wfapi_headers) 
        
        print(json.dumps(self.wfapi_ret.json(), indent=2, ensure_ascii=False)) 
        if not __debug__:
            print("------WF-API------")
            print( "WF-API_res_code: " + str( self.wfapi_ret.status_code ) )
            print(json.dumps(self.wfapi_ret.json(), indent=2, ensure_ascii=False)) 
        
        
        ### web応答が200か201で無ければ、失敗にする
        if ( self.wfapi_ret.status_code != self.HTTP_OK ) and ( self.wfapi_ret.status_code != self.HTTP_OK2 ) :
        
            print("ワークフロー取得エラーが発生した。" + os.linesep )
            raise OSError("Cannot got Workflow Error." + os.linesep )
        
        
        self.wfdata = self.wfapi_ret.json()
        self.myrevisions = self.wfdata["revisions"] #revisionsを取り出す
        print( "revi_len: " + str( len( self.myrevisions ) )  )
        
        # 一番大きいリビジョンを探す
        i=0
        for chwf in self.myrevisions:
            
            if self.wf_update < chwf["workflow_revision"]:
                self.wf_update = chwf["workflow_revision"]
                self.sel_wf = i
            
            i = i + 1
        
        
        print("sel_wf:" + str( self.sel_wf ) )
        
        self.wf_name = self.myrevisions[self.sel_wf]["name"] #ワークフロー名を設定する
        self.wf_description = self.myrevisions[self.sel_wf]["description"] #ワークフローの説明を設定する
        
        
        #ポートを取得
        self.has_port = self.myrevisions[self.sel_wf]["miwf"]["mainWorkflow"]["diagramModel"]["nodeDataArray"]
        
        print("has_port_len: " + str( len( self.has_port ) ) )
        #pprint.pprint( has_port , width=40 )
        
        
        # 入出力ポートを列挙する
        i=0
        #print( "ここからポート" )
        for is_port in self.has_port:
            portdata = {}
            
            # 入力ポート
            if is_port["category"] == "inputdata" : 
                
                portdata["port_name"] = is_port["name"]
                portdata["descriptor_id"] = is_port["descriptor"]
                portdata["description"] = is_port["description"]
                
                self.inputport.append( portdata )
            
            # 出力ポート
            elif is_port["category"] == "outputdata" : 
                
                portdata["port_name"] = is_port["name"]
                portdata["descriptor_id"] = is_port["descriptor"]
                portdata["description"] = is_port["description"]
                
                self.outputport.append( portdata )
            
            # 該当なし
            else:
                pass
            
            i = i + 1
            
        #print( "ここまでポート" )
        print( "input_port_len:" + str( len( self.inputport ) ) )
        print( "output_port_len:" + str( len( self.outputport ) ) )
        
        
    
    ### ワークフローに予測モデル名を設定する
    def setPredictionModel( self, pmid_uri ):
        self.pm_id = pmid_uri[self.PRED_ID_LEN:]
        self.wfdata["prediction_model_id"] = pmid_uri
    
    
    ### ワークフロー情報を更新する
    def upWrokflowData( self ):
        if self.pm_id is None:
            print( "No pmid. Cannot Update WorkFlow." )
            return
        
    
    
    ### チェッカー関数
    
    ### toString()
    def __str__(self):
    
        tmpstr = "------myWorkFlowData dump------" + os.linesep
        if self.acsinfo is not None:
            tmpstr += "WF_acs_uri: " + self.acsinfo.wfapi_acsuri + os.linesep
        else :
            tmpstr += "WF_acs_uri is not exist." + os.linesep
        
        if self.wfapi_ret is not None:
            tmpstr += "WF-API_res_code: " + str( self.wfapi_ret.status_code ) + os.linesep
        else :
            tmpstr += "WF-API_res_code is not exist." + os.linesep
        
        if self.wfapi_ret is not None:
            tmpstr += "WF_JSON-data: " + os.linesep + json.dumps(self.wfapi_ret.json(), indent=2, ensure_ascii=False  ) + os.linesep
        else :
            tmpstr += "WF_JSON-data is not exist." + os.linesep
        
        if self.wf_name is not None:
            tmpstr += "WF-name: " + self.wf_name + os.linesep
        else:
            tmpstr +="WF-name is not exist." + os.linesep
        
        if self.wf_description is not None:
            tmpstr += "WF-Desc: " + self.wf_description + os.linesep
        else:
            tmpstr += "WF-Desc is not exist." + os.linesep
        
        if self.pm_id is not None:
            tmpstr += "PMID: " + self.pm_id + os.linesep
        else:
            tmpstr += "PMID is not exist." + os.linesep
        
        tmpstr += "------End myWorkFlowData dump------" + os.linesep
        
        ### WF関係の情報をダンプ
        return tmpstr
    
    
    ### デストラクタ
    def __del__(self):
        self.wf_session.close() #WF-APIのセッションを終了
    
    

# Function section
##VBのDoEvents的なやつ
def taiki():
    myextsync = "/bin/sync"  #for linux
    time.sleep( 0.5 )
    sys.stdout.flush()
    sys.stderr.flush()
    
    if os.path.isfile( myextsync[1:-1] ):
    
        # Linux用sync、python3.6用
        subprocess.run( myextsync, shell=True )
    
    else :
    
        print( "sync program not found.." )
    
    time.sleep( 0.5 )


## 強制メモリコンパクション
def memclean():
    ## Linux用、当然root権限が必要
    subprocess.run( '"echo 3 > /proc/sys/vm/drop_caches"', shell=True )



# -- main flow --

# init

## variables
mytoken = "<myToken>" #東大運用環境utrootユーザーのtoken
target_host = "chooselocation.mintsys.jp" #MIntシステムのアクセス先
myport = 443 #MIntシステムのWF-APIポート
wf_api_ver = "v2" #WF-APIバージョン
wf_api_name = "workflow-api" #WF-APIの名前（変わることあるのか？）
inv_api_ver = "v5" #インベントリAPIのバージョン
inv_api_name = "inventory-api" #インベントリAPIの名前（変わることあるのか？）
inv_up_api_name = "inventory-update-api" #インベントリ更新API名（変わることはあるのか？）
workflow_id = "" #ワークフローID
desc_id = "" #デスクリプターID
pm_id="" #ワークフロー予測モデルID


## CONSTS




## progress args
parser = argparse.ArgumentParser(description='How to Use this command.')
parser.add_argument('-t','--token')
parser.add_argument('-o','--host')
parser.add_argument('-p','--port', type=int)
parser.add_argument('-v','--wfapiver')
parser.add_argument('-n','--wfapiname' )
parser.add_argument('-u','--invapiver')
parser.add_argument('-m','--invapiname' )
parser.add_argument('-l','--invupapiname' )
parser.add_argument('-w','--wfid' )
args = parser.parse_args()

if args.token:
    mytoken = args.token

if args.host:
    target_host = args.host

if args.port:
    myport = int( args.port )

if args.wfapiver:
    wf_api_ver = args.wfapiver

if args.wfapiname:
    wf_api_name = args.wfapiname

if args.invapiver:
    inv_api_ver = args.invapiver

if args.invapiname:
    inv_api_name = args.invapiname

if args.invupapiname:
    inv_up_api_name = args.invupapiname

if args.wfid:
    workflow_id = args.wfid



##print config.
if __debug__:
#if not __debug__:
    print( "--- args ----" )
    print( "host: " + target_host )
    print( "port: " + str( myport ) )
    print( "wf_api_ver: " + wf_api_ver )
    print( "wf_api_name: " + wf_api_name )
    print( "inv_api_ver: " + inv_api_ver )
    print( "inv_api_name: " + inv_api_name )
    print( "inv_up_api_name" + inv_up_api_name )
    print( "workflow_id: " + workflow_id )
    print( "token: " + mytoken )
    print( "--- end args ---" )


#pre process
## アクセス情報を作って、ワークフロークラスを初期化する
print( "アクセス情報を作って、ワークフロークラスを初期化する" )
myMIacs = myAccessInfo( target_host, myport, mytoken, wf_api_ver, wf_api_name, inv_api_ver, inv_api_name, inv_up_api_name , workflow_id, desc_id )
MyWFdata = myWorkFlowData( myMIacs )

## ワークフロー情報を取得する
print( "ワークフロー情報を取得する" )
MyWFdata.getWorkflowData()


# インベントリクラスを初期化する
print( "インベントリクラスを初期化する" )
MyInvdata = myInventoryData( myMIacs, MyWFdata )

# インベントリに登録する予測モデルを作る
print( "インベントリに登録する予測モデルを作る" )
MyInvdata.mkPredictionModelData()

# 予測モデル情報を送信する
print( "予測モデル情報を送信する" )
MyInvdata.upPredictionModelData()


# 予測モデルの値を取得する
pm_id = MyInvdata.getPredictionModelID()
print( "予測モデルID: " + pm_id + os.linesep )

# 予測モデルの値をWFに設定する
MyWFdata.setPredictionModel( MyInvdata.getPredictionModelID_URI() )

"""
# 予測モデル値を設定したワークフロー情報を送信する
#MyWFdata.upWrokflowData()



# ToString() メソッドデバッグ用
print( "access info:" )
print( myMIacs )
print( "access info end" + os.linesep +"WF info:" )
print( MyWFdata )
print( "WF info end" + os.linesep + "Inv info:" )
print( MyInvdata )
print( "Inv info end" + os.linesep )
"""

#main process




#post process


#finalize
print("prediction configure successed.")

#TODO
# * 
# * 
# * 

