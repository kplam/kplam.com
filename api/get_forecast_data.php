<?php
	session_start();

	include_once '../admin/function/db_conf.php';

	@$date = $_GET['date'];
	//正则与默认值
	$datedef = date('Y-m-d',strtotime('-180 day'));
	if (preg_match ("/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/", $date, $parts))
           { if(checkdate($parts[2],$parts[3],$parts[1]))
	   $date = $date;
	else
	   $date = $datedef;}
	else
	   $date = $datedef;
	
	if(isset($_SESSION['user_id'])){

	$result = $conn -> prepare("SELECT * FROM `forecast` LEFT JOIN stocklist ON `forecast`.`code` = `stocklist`.`证券代码` WHERE (`date` > ?) AND ( `预告类型` = '预增' OR `预告类型` = '预盈' OR `预告类型` = '减亏') AND `stocklist`.`证券代码`is not null ORDER BY `date` DESC");
	$result -> bind_param("s", $date);
	$result -> execute();
	$result->store_result();
	$result->bind_result($code,$a_date,$report,$change,$type,$profit_lp,$fr_date,$code2,$name,$market,$status,$pinyin);
	
	$data = array();

	if($result->num_rows > 0) {
		 while($row = $result->fetch()) {
			
			$data[] = array('code_name'=>$name."<br>".$code,
							'code'=> $code,
							'name'=>$name,
							'report'=>$report,
							'type_change'=>$type."<br>".$change,
							'type'=>$type,
							'change'=>$change,
							'a_date'=>$a_date,
							'fr_date'=>$fr_date,
							'profit_lp'=>$profit_lp
				);
		}
	}


	echo json_encode($data,JSON_UNESCAPED_UNICODE);
	}else{
		exit();
	}
	
?>