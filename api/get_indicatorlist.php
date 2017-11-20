<?php

	session_start();
    include_once '../admin/function/db_conf.php';

	
	if(isset($_SESSION['user_id'])){

		$result = $conn -> prepare("SELECT * FROM `indicator`");
		$result -> execute();
		$result->store_result();
		$result->bind_result($name,$short,$input,$output,$main);

		$data = array();

		if($result->num_rows > 0) {
			 while($row = $result->fetch()) {
			     if ($main ==1){
				$data[] = array('main_name'=>$name,
								'main'=> $short
					);}
					else{
                        $data[] = array('sub_name'=>$name,
                            'sub'=> $short);
                    }
			}
		}
		echo json_encode($data,JSON_UNESCAPED_UNICODE);		
	} else {
		$data[] = array('status'=> 'No Login',);
		echo json_encode($data,JSON_UNESCAPED_UNICODE);
		exit();
	}



	
?>