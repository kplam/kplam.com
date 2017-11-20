<?php
/**
 * Created by PhpStorm.
 * User: KPLAM
 * Date: 2017/11/14 0014
 * Time: 20:27
 */
session_start();
include_once '../admin/function/db_conf.php';
@$keyword = $_GET['keyword'];
$keyword = "%".$keyword."%";
if(isset($_SESSION['user_id'])){

    $result = $conn -> prepare("SELECT * FROM `basedata` WHERE CONCAT_WS(',',`证券简称`,`公司名称`,`公司简介`,`省份`,`城市`,`注册地址`,`办公地址`,`经营分析`,`简史`,`核心题材`,`所属主题`,`所属概念`) LIKE ?");
    $result -> bind_param("s", $keyword);
    $result -> execute();
    $result->store_result();
    $result->bind_result($code,$name,$fullname,$ename,$usedname,$brief,$founddate,$regid,$regcapital,$legal_representative,
        $csrcclassification,$member,$generalmanage,$boardsecretary,$province,$city,$regaddr,$officeaddr,$postalcode,$tel,
        $fax,$email,$website,$auditor,$counsel,$mainbusiness,$history,$point,$subject,$concept,$ipodate,$ipoprice,$lastupdate);

    $data = array();

    if($result->num_rows > 0) {
        while($row = $result->fetch()) {

            $data[] = array('code'=>$code,'name'=>$name,'fullname'=>$fullname,
                'ename'=>$ename,'usedname'=>$usedname,'brief'=>$brief,
                'founddate'=>$founddate,'regid'=>$regid,'regcapital'=>$regcapital,
                'legal_erpresentative'=>$legal_representative,'csrcclassification'=>$csrcclassification,
                'member'=>$member,'generalmanage'=>$generalmanage,'boardsecretary'=>$boardsecretary,
                'province'=>$province,'city'=>$city,'regaddr'=>$regaddr,'officeaddr'=>$officeaddr,
                '$postalcode'=>$postalcode,'tel'=>$tel,'fax'=>$fax,'email'=>$email,
                'website'=>$website,'auditor'=>$auditor,'counsel'=>$counsel,'mainbusiness'=>$mainbusiness,
                'history'=>$history,'point'=>$point,'subject'=>$subject,'concept'=>$concept,
                'ipodate'=>$ipodate,'ipoprice'=>$ipoprice,'lastupdate'=>$lastupdate
            );
        }
    }


    echo json_encode($data,JSON_UNESCAPED_UNICODE);
}else{
    exit();
}

?>