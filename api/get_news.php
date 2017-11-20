<?php
/**
 * Created by PhpStorm.
 * User: KPLAM
 * Date: 2017/11/14 0014
 * Time: 21:30
 */
session_start();
if(isset($_SESSION['user_id'])){
    include_once '../admin/function/db_conf.php';
    @$date=$_GET['date'];
    //正则与默认值
    $datedef = date('Y-m-d',strtotime('-3 day'));
    if (preg_match ("/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/", $date, $parts))
    { if(checkdate($parts[2],$parts[3],$parts[1]))
        $date = $date;
    else
        $date = $datedef;}
    else
        $date = $datedef;

    $sql = "SELECT *  FROM `news` WHERE `datetime` >= ? order by `datetime` desc;";
    $result = $conn -> prepare($sql);
    $result -> bind_param('s',$date);
    $result -> execute();
    $result->store_result();
    $result->bind_result($id,$source,$type,$title,$link,$content,$time);
    $data= array();
    if($result->num_rows > 0) {
        //while ($row = mysqli_fetch_assoc($result)){
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
        //var_dump($data);
}else{
    exit();
}
?>