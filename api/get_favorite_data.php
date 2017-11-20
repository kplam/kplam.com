<?php
	
	session_start();

	include_once '../admin/function/db_conf.php';

	if(isset($_SESSION['user_id'])){

		$sql = "SELECT * FROM favorite WHERE user_id = ?  ORDER BY add_date DESC;";
		$stmt = mysqli_stmt_init($conn);
		
		if(!mysqli_stmt_prepare($stmt, $sql)) {
			    exit();
		} else {
				//Bind parameters to the placeholder
				mysqli_stmt_bind_param($stmt, "s", $_SESSION['user_id']);
				//Run query in database
				mysqli_stmt_execute($stmt);
				$result = mysqli_stmt_get_result($stmt);

				//echo "The number of record is ". mysqli_num_rows($result);
				$data = array();
				while ($row = mysqli_fetch_assoc($result)){
					$data[] = array(
								'favorite_id'=> $row['favorite_id'],
								'user_id'=> $row['user_id'],
								'stock_code'=> $row['stock_code'],
								'stock_name'=> $row['stock_name'],
								'add_date'=> $row['add_date'],

					);
				}
				echo json_encode($data,JSON_UNESCAPED_UNICODE);
		}

	}else {
		exit();
	}
?>