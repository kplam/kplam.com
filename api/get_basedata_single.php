<?php

	session_start();
	include_once '../admin/function/db_conf.php';

  	$code = $_GET['code'];
	if (preg_match ("/^([0-9]{6})$/", $code, $parts)){
	   
	   $code = $code;

	} else{
	   $data[] = array('status'=> 'wrong code',);
	   echo json_encode($data,JSON_UNESCAPED_UNICODE);
	   exit();
	}


	if(isset($_SESSION['user_id'])){
		
		$sql = "SELECT `证券简称`, `经营分析`, `核心题材`, `所属主题`, `所属概念` FROM `basedata` WHERE `证券代码`=?;";
		$result = $conn -> prepare($sql);
		$result -> bind_param('s',$code);
		$result -> execute();
		$result->store_result();
		$result->bind_result($name,$mainbusiness,$point,$subject,$concept);

		$data= array();
		if($result->num_rows > 0) {
			 while($row = $result->fetch()) {
			 	//var_dump($point);
				$data[] = array(
								'code'=>$code,
								'name'=>$name,
								'Mainbuiness'=>$mainbusiness,
								'point'=>$point,
								'subject'=>$subject,
								'concept'=>$concept,
					);
			}
		}
		echo json_encode($data,JSON_UNESCAPED_UNICODE);
	} else {
		$data[] = array('status'=> 'No Login',);
		echo json_encode($data,JSON_UNESCAPED_UNICODE);
		exit();
	}

?>