<?php

	session_start();
    include_once '../admin/function/db_conf.php';
	$code = $_GET['code'];
	if (preg_match ("/^([0-9]{6})$/", $code, $parts)){
	   $code = "%".$code."%";
	} else{
	   $data[] = array('status'=> 'wrong code',);
	   echo json_encode($data,JSON_UNESCAPED_UNICODE);
	   exit();
	}


	if(isset($_SESSION['user_id'])){
		
		$sql = "SELECT *  FROM `news` WHERE `content` LIKE ? order by `datetime` desc;";
		$result = $conn -> prepare($sql);
		$result -> bind_param('s',$code);
		$result -> execute();
		$result->store_result();
		$result->bind_result($id,$source,$type,$title,$link,$content,$time);

		$data= array();
		if($result->num_rows > 0) {
			 while($row = $result->fetch()) {
				$data[] = array(
								'type'=>$type,
								'title'=>$title,
								'content'=>$content,
								'time'=>$time,
								'link'=>$link,
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