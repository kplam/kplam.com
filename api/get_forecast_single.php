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

		$result = $conn -> prepare("SELECT * FROM `forecast` WHERE `code` = ? ORDER BY `date` DESC");
		$result -> bind_param("s",$code);
		$result -> execute();
		$result->store_result();
		$result->bind_result($code,$a_date,$report,$change,$type,$profit_lp,$fr_date);

		$data = array();

		if($result->num_rows > 0) {
			 while($row = $result->fetch()) {
				$data[] = array(
								'code'=> $code,
								'report'=>$report,
								'type'=>$type,
								'change'=>$change,
								'a_date'=>$a_date,
								'fr_date'=>$fr_date,
								'profit_lp'=>$profit_lp
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