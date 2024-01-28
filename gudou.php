<?php
session_start();
error_reporting(0);
header('Content-Type:text/html;charset=UTF-8');
$id = isset($_GET['id'])?$_GET['id']:'cctv1';
$n =[  
     //央视
    "cctv1" => ["CCTV1HD_1500"],   //CCTV1综合HD
  "cctv1hd" => ["CCTV1HD_3000"],   //CCTV1综合HD
  "cctv2" => ["CCTV2HD_3000"],   //CCTV2财经HD
  "cctv2hd" => ["CCTV2HD_7000"],   //CCTV2财经HD
  "cctv3" => ["CCTV3HD_1500"],   //CCTV3综艺HD
  "cctv3hd" => ["CCTV3HD_3000"],   //CCTV3综艺HD
  "cctv4" => ["CCTV-4HD_1500"],   //CCTV4中文国际
  "cctv4hd" => ["CCTV-4HD_7500"],   //CCTV4国际HD
  "cctv5" => ["CCTV5HD_1500"],   //CCTV5体育HD
  "cctv5hd" => ["CCTV5HD_3000"],   //CCTV5体育HD
  "cctv5p" => ["CCTV5plusHD_1500"],   //CCTV5+体育赛事HD
  "cctv5phd" => ["CCTV5plusHD_3000"],   //CCTV5+体育赛事HD
  "cctv6" => ["CCTV6HD_1500"],   //CCTV6电影HD
  "cctv6hd" => ["CCTV6HD_3000"],   //CCTV6电影HD
  "cctv7" => ["CCTV7HD_1500"],   //CCTV7国防军事HD
  "cctv7hd" => ["CCTV7HD_3000"],   //CCTV7国防军事HD
  "cctv8" => ["CCTV8HD_1500"],   //CCTV8电视剧HD
  "cctv8hd" => ["CCTV8HD_3000"],   //CCTV8电视剧HD
  "cctv9" => ["CCTV9HD_1500"],   //CCTV9纪录HD
  "cctv9hd" => ["CCTV9HD_3000"],   //CCTV9纪录HD
  "cctv10" => ["CCTV10HD_1500"],   //CCTV10科教HD
  "cctv10hd" => ["CCTV10HD_3000"],   //CCTV10科教HD
  "cctv11" => ["CCTV-11HD_1500"],   //CCTV11戏曲
  "cctv11hd" => ["CCTV-11HD_7500"],   //CCTV11戏曲HD
  "cctv12" => ["CCTV12HD_1500"],   //CCTV12社会HD
  "cctv12hd" => ["CCTV12HD_3000"],   //CCTV12社会HD
  "cctv13" => ["1013_1500"],   //CCTV13新闻
  "cctv13hd" => ["1613"],   //CCTV13新闻HD
  "cctv14" => ["CCTV14HD_1500"],   //CCTV14少儿HD
  "cctv14hd" => ["CCTV14HD_3000"],   //CCTV14少儿HD
  "cctv15" => ["CCTV15music_1500"],   //CCTV15音乐
  "cctv15hd" => ["CCTV-15HD_1500"],   //CTV15音乐HD
  "cctv16" => ["1617_1500"],   //CCTV16奥林匹克
  "cctv164k" => ["4010"],   //CCTV16奥林匹克4K
  "cctv17" => ["CCTV17_2000"],   //CCTV17农村农业
  "cctv17hd" => ["CCTV17HD"],   //CCTV117农村农业HD
  "cctv4k" => ["CCTVHHD4K_38000"],   //CCTV4K超高清
  "hjjc" => ["huaijiujuchang_1500"],   //怀旧剧场
  "fyjc" => ["fengyunjuchang_1500"],   //风云剧场
  "fyyy" => ["fengyunyinyue_1500"],   //风云音乐
  "fyzq" => ["fengyunzuqiu_1500"],   //风云足球
  "cgtn" => ["CCTV15news_1500"],   //CGTN
  "sh" => ["shuhua_1500"],   //书画
  "zgtq" => ["zgqixiang_1500"],   //中国天气
   //中国教育
  "cetv1" => ["CETV-1_1500"],   //CETV1
  "cetv1hd" => ["CETV1HD_1500"],   //CETV1HD
  "cetv4" => ["CETV-4_1500"],   //CETV4
   //CHC系列
  "chcgq" => ["CHCHD_7000"],   //CHC高清电影
  "chcjt" => ["CHChometheatre_1500"],   //CHC家庭影院
  "chcdz" => ["CHCactionmovie_1500"],   //CHC动作电影
  //卫视
  "bjws" => ["beijingHD_1500"],   //北京卫视
  "bjhd" => ["beijingHD_3000"],   //北京卫视HD
  "dfws" => ["dongfangHD_1500"],   //东方卫视
  "dfhd" => ["dongfangHD_3000"],   //东方卫视HD
  "tjws" => ["1415_800"],   //天津卫视
  "tjhd" => ["1415_4500"],   //天津卫视HD
  "cqws" => ["chongqingHD_1500"],   //重庆卫视
  "cqhd" => ["chongqingHD_3000"],   //重庆卫视HD
  "hljws" => ["heilongjiangHD_1500"],   //黑龙江卫视
  "hljhd" => ["heilongjiangHD_3000"],   //黑龙江卫视HD
  "jlws" => ["jilinweishi_1500"],   //吉林卫视
  "jlhd" => ["jilinHD_7000"],   //吉林卫视HD
  "ybws" => ["yanbianweishi_2000"],   //延边卫视
  "lnws" => ["liaoningHD_1500"],   //辽宁卫视
  "lnhd" => ["liaoningHD_3000"],   //辽宁卫视HD
  "nmws" => ["neimenggu_1500"],   //内蒙古卫视
  "nxws" => ["ningxiaweishi_800"],   //宁夏卫视
  "gsws" => ["1236_1500"],   //甘肃卫视
  "qhws" => ["qinghaiweishi_1500"],   //青海卫视
  "sxws" => ["1248_1500"],   //陕西卫视
  "hbws" => ["1426"],   //河北卫视
  "hbhd" => ["1426_4500"],   //河北卫视HD
  "sxiws" => ["shanxi_1500"],   //山西卫视
  "sdws" => ["1416_1500"], //山东卫视
  "sdhd" => ["1416_4500"], //山东卫视HD
  "ahws" => ["anhuiHD_1500"],   //安徽卫视
  "ahhd" => ["anhuiHD_3000"],   //安徽卫视HD
  "hnws" => ["henan_800"], //河南卫视
  "hubws" => ["hubeiHD_1500"],   //湖北卫视
  "hubhd" => ["hubeiHD_3000"], //湖北卫视HD
  "hunws" => ["hunanHD_1500"],   //湖南卫视
  "hunhd" => ["hunanHD_3000"],   //湖南卫视HD
  "jxws" => ["jiangxi_1500"],   //江西卫视
  "jxhd" => ["jiangxiHD_7000"],   //江西卫视HD
  "jsws" => ["jiangsuHD_1500"],   //江苏卫视
  "jshd" => ["jiangsuHD_3000"],   //江苏卫视HD
  "zjws" => ["zhejiangHD_1500"],   //浙江卫视
  "zjhd" => ["zhejiangHD_3000"],   //浙江卫视HD
  "dnws" => ["dongnan_1500"],   //东南卫视
  "dnhd" => ["dongnanweishiHD_1500"],   //东南卫视HD
  "gdws" => ["guangdongHD_1500"],   //广东卫视
  "gdhd" => ["guangdongHD_3000"],   //广东卫视HD
  "szws" => ["shenzhenHD_1500"],   //深圳卫视
  "szhd" => ["shenzhenHD_3000"],   //深圳卫视HD
  "dwqws" => ["gdnanfang_1500"],   //大湾区卫视
  "gxws" => ["guangxiweishi_1500"],   //广西卫视
  "gxhd" => ["guangxi_7500"],   //广西卫视HD
  "ynws" => ["1239_1500"],   //云南卫视
  "gzws" => ["guizhouHD_1500"],   //贵州卫视
  "gzhd" => ["guizhouHD_3000"],   //贵州卫视HD
  "scws" => ["sichuanHD_1500"],   //四川卫视
  "schd" => ["sichuanHD_3000"],   //四川卫视HD
  "xjws" => [" xinjiang_1500"], //新疆卫视
  "btws" => ["1249_1500"],   //兵团卫视
  "xzws" => ["xizangweishi_1500"],   //西藏卫视
  "hinws" => ["lvyouweishi_1500"],   //海南卫视
  "hinhd" => ["1451_1500"],   //海南卫视HD
  "ssws" => ["1453_4500"],   //三沙卫视
  //地方
  "kkse" => ["kakushaoer_1500"],   //卡酷少儿
  "hqqg" => ["huanqiuqiguan_1500"],   //环球奇观
  "jbty" => ["jinbaotiyuHD_1500"],   //劲爆体育
  "jbtyhd" => ["jinbaotiyuHD_3000"],   //劲爆体育HD
  "ly" => ["quanjishi_1500"],   //乐游
  "lyhd" => ["quanjishiHD_7000"],   //乐游HD
  "dfcj" => ["1941_4500"],   //东方财经
  "fztd" => ["fazhitiandi_1500"],   //法治天地
  "dsjc" => ["dushijuchang_1500"],   //都市剧场
  "dmxc" => ["dongmanxiuchang_1500"],   //动漫秀场
  "mlzq" => ["meiliyinyue_1500"],   //魅力足球
  "jsxt" => ["jinsepindao_1500"],   //金色学堂
  "hhxd" => ["1258_1500"], //哈哈炫动
  "xsj" => ["xinshijuegaoqing_3000"],   //新视觉
  "xdm" => ["xindongman_1500"],   //新动漫
  "wwbk" => ["1939_7500"],   //文物宝库
  "wssj" => ["1938_7500"],   //武术世界
  "lypd" => ["1937_7500"],   //梨园频道
  "jykt" => ["jinyingkatong_1500"],   //金鹰卡通
  "klcd" => ["huanxiaojuchang_1500"],   //快乐垂钓
  "xfpy" => ["pingyu_1500"],   //先锋乒羽
  "ymkt" => ["youmankatong_1500"],   //优漫卡通
  //广东
  "gdzy4k" => ["GDZYHD4K_38000"],   //广东综艺4K
  "gdzj" => ["gdzhujiang_1500"],   //广东珠江
  "gdms" => ["gdpublic_1500"],   //广东民生
  "gdxw" => ["gdnews_1500"],   //广东新闻
  "gdty" => ["gdsports_1500"],   //广东体育
  "gdtyhd" => ["gdsportsHD_3000"],   //广东体育HD
  "gdjjkj" => ["gdjingjikejiao_1500"],   //广东经济科教
  "gdjjkjhd" => ["gdjingjikejiaoHD_1500"],   //广东经济科教HD
  "gdys" => ["gdyingshi_1500"],   //广东影视
  "gdse" => ["gdshaoer_1500"],   //广东少儿
  "lnxq" => ["1460_4500"],   //岭南戏曲
  "jjkt" => ["gdjiajiacartoon_1500"],   //嘉佳卡通
  "gdds" => ["GHDdaoshi_3000"],   //广东导视
  "gzzh" => ["1432_1500"],   //广州综合
  "gzxw" => ["1433_1500"],   //广州新闻
  "gzfz" => ["gzeconomic_1500"],   //广州法治
  "gzjs" => ["gzcompetition_1500"],   //广州竞赛
  "gzys" => ["gzfilms_1500"],   //广州影视
  "zctv" => ["2079"],   //增城电视台
  "czzh" => ["chaozhouyitao_1500"],   //潮州综合
  "czms" => ["chaozhouertao_1500"],   //潮州民生
  "cazh" => ["chaoanzongheHD_4500"],   //潮安综合
  "rpzh" => ["raopingtaiHD_4500"],   //饶平综合HD
  "fszh" => ["foshannews_1500"],   //佛山综合
  "fszhhd" => ["foshanzongheHD_4500"],   //佛山综合HD
  "fsgg" => ["foshanyingshi_1500"],   //佛山公共
  "fsgghd" => ["foshangonggongHD_4500"],   //佛山公共HD
  "fsys" => ["foshanyingshiHD_4500"],   //佛山影视
  "fssd" => ["shundetai_2000"],   //顺德台
  "fsnh" => ["nanhaitai_2000"],   //南海台
  "dg1" => ["dongguanyitao_1500"],   //东莞新闻综合
  "dg1hd" => ["2121_11000"],   //东莞新闻综合HD
  "dg2" => ["dongguanertao_1500"],   //东莞生活资讯
  "dg2hd" => ["2122_11000"],   //东莞生活资讯
  "hy1" => ["heyuanyitao_1500"],   //河源综合
  "hy1hd" => ["heyuanzongheHD_4500"],   //河源综合HD
  "hy2" => ["heyuanertao_1500"],   //河源公共
  "hz1" => ["2301_1500"],   //惠州一套
  "hz1hd" => ["2314_4500"],   //惠州一套HD
  "hz2" => ["2302_1500"],   //惠州二套
  "hz2hd" => ["2316_4500"],   //惠州二套HDHD
  "blzh" => ["boluozonghe_1500"],   //博罗综合
  "blzhb" => ["2305"],   //博罗综合
  "blzhhd" => ["2305_4500"],   //博罗综合HD
  "hdzh" => ["huidongHD_800"],   //惠东综合HD
  "hyzh" => ["huiyangtai_2000"],   //惠阳综合
  "jmzh" => ["3712_1500"],   //江门综合
  "jmzhhd" => ["jiangmenzongheHD_4500"],   //江门综合HD
  "jmqxsh" => ["jiangmenyitao_1500"],   //江门侨乡生活
  "hszh" => ["3709"],   //鹤山综合
  "xhzh" => ["xinhui_1500"],   //新会综合
  "jyzh" => ["jieyangyitao_1500"],   //揭阳综合
  "jyzhhd" => ["jieyangzongheHD_4500"],   //揭阳综合HD
  "jysh" => ["jieyangertao_1500"],   //揭阳生活
  "jyshhd" => ["jieyanggonggongHD_4500"],   //揭阳生活HD
  "jdzh" => ["jiedongzonghe_2000"],   //揭东综合
  "mmzh" => ["3012_1500"],   //茂名综合
  "mmwhsh" => ["3013_1500"],   //茂名文化生活
  "mmwhsh2" => ["3013_4500"],   //茂名文化生活2
  "hzzh" => ["huazhoutai_800"],   //化州综合
  "xyzh" => ["xinyigaoqing_4500"],   //信宜综合
  "mz1" => ["meizhou1HD_4500"],   //梅州1
  "mz2" => ["meizhou2HD_4500"],   //梅州2
  "mzds" => ["meizhoudaoshiHD_7500"],   //梅州导视
  "mxzh" => ["meixianHD_4500"],   //梅县综合
  "py1" => ["pingyuan1_2000"],   //平远-1
  "whzh" => ["wuhua1HD_7500"],   //五华综合
  "xnzh" => ["xingning1_2000"],   //兴宁综合
  "qyxwzh" => ["qingyuanzonghe_1500"],   //清远新闻综合
  "qyxwzhhd" => ["qingyuanzongheHD_4500"],   //清远新闻综合HD
  "qywlsh" => ["qingyuangongong_1500"],   //清远文旅生活
  "qywlshhd" => ["qingyuangonggongHD_4500"],   //清远文旅生活HD
  "fgzh" => ["2405_2000"],   //佛冈综合
  "ydzh" => ["yingdezonghe_800"],   //英德综合
  "stxwzh" => ["shantouyitaogaoqing_1500"],   //汕头新闻综合
  "stxwzh2" => ["shantouyitaogaoqing_4500"],   //汕头新闻综合2
  "stjjsh" => ["shantouertaogaoqing_1500"],   //汕头经济生活
  "stjjsh2" => ["shantouertaogaoqing_4500"],   //汕头经济生活2
  "stwlty" => ["2508_1500"],   //汕头文旅体育
  "stwlty2" => ["2508_4500"],   //汕头文旅体育2
  "swxwzh" => ["shanweiyitao_1500"],   //汕尾新闻综合
  "swwhsh" => ["shanweiertao_1500"],   //汕尾文化生活
  "hfzh" => ["haifengzonghe_800"],   //海丰综合
  "sgzh" => ["shaoguanzonghe_1500"],   //韶关综合
  "sglssh" => ["shaoguangonggong_1500"],   //韶关绿色生活
  "sgsx" => ["2641"],   //始兴综合
  "yfzh" => ["yunfuyitao_1500"],   //云浮综合
  "yfwl" => ["yunfuertao_1500"],   //云浮文旅
  "zh1" => ["zhuhaiHD1_1500"],   //珠海一套
  "zh1hd" => ["zhuhaiHD1_4500"],   //珠海一套HD
  "zh2" => ["zhuhaiHD2_1500"],   //珠海二套
  "zh2hd" => ["zhuhaiHD2_4500"],   //珠海二套HD
  "dmrm" => ["2207_4500"],   //斗门融媒
  "zjzh" => ["zhanjiangzonghe_1500"],   //湛江综合
  "zjgg" => ["zhanjianggonggong_1500"],   //湛江公共
  "ljzh" => ["3209_7500"],   //廉江综合
  "zqzh" => ["zhaoqingyitao_1500"],   //肇庆综合
  "zqshfw" => ["zhaoqingertao_1500"],   //肇庆生活服务
  "hjzh" => ["2805_2000"],   //怀集综合
  "zszh" => ["zhongshanyitao_1500"],   //中山综合
  "zszhhd" => ["3665_4500"],   //中山综合HD
  "zsxswh" => ["zhongshanertao_1500"],   //中山香山文化
  "zsxswhhd" => ["3663_4500"],   //中山香山文化HD
  "zsjy" => ["3664_4500"],   //中山教育
  //港澳
  "fhzw" => ["fhzw_1500"],   //凤凰中文
  "fct" => ["xgfeicui_1500"],   //翡翠台
  "mzt" => ["xgmingzhu_1500"],   //明珠台
  "fcthd" => ["1350_4500"],   //翡翠台HD
  "mzthd" => ["1351_4500"],   //明珠台HD
  "asam" => ["1352_4500"], //澳视澳门
  "xkws" => ["xingkong_1500"],   //星空卫视
  "ayws" => ["aoya_1500"],   //澳亚卫视
  //其他
  "qssh" => ["QSSHHD_7000"],   //求索生活
  "qsjl" => ["QSJLHD_7000"],   //求索纪录
  "qskx" => ["qiusuokexueHD_7000"],   //求索科学
  "qsdw" => ["QSDWHD_7000"],   //求索动物
    ];
//$id=$_GET['id'];
$user='17199741419';
$ptoken='w14L5ppGYYzipwiIRQpgdA==';
$pserialnumber='865372026096088';
$t=time();
$nonce=rand(100000,999999);
$str='sumasalt-app-portalpVW4U*FlS'.$t.$nonce.$user;
$hmac=substr(sha1($str),0,10);
$onlineip=$_SERVER['REMOTE_ADDR'];
$info='ptype=1&plocation=001&puser='.$user.'&ptoken='.$ptoken.'&pversion=030104&pserverAddress=portal.gcable.cn&pserialNumber='.$pserialnumber.'&pkv=1&ptn=Y29tLnN1bWF2aXNpb24uc2FucGluZy5ndWRvdQ&pappName=GoodTV&DRMtoken='.$ptoken.'&epgID=&authType=0&secondAuthid=&t='.$ptoken.'&pid=&cid=&u='.$user.'&p=8&l=001&d='.$pserialnumber.'&n='.$n[$id][0].'&v=2&hmac='.$hmac.'&timestamp='.$t.'&nonce='.$nonce;
$url='http://portal.gcable.cn:8080/PortalServer-App/new/aaa_aut_aut001';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, TRUE);
curl_setopt($ch, CURLOPT_POSTFIELDS, $info);
curl_setopt($ch, CURLOPT_USERAGENT, "Apache-HttpClient/UNAVAILABLE (java 1.4)");
curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-FORWARDED-FOR:'.$onlineip, 'CLIENT-IP:'.$onlineip));
$res = curl_exec($ch);
curl_close($ch);
$uas=parse_url($res);
parse_str($str, $array);
parse_str($uas["query"], $parsedArray);
$token = "?t={$parsedArray['t']}&u={$parsedArray['u']}&p={$parsedArray['p']}&pid=&cid={$parsedArray['cid']}&d={$parsedArray['d']}&sid={$parsedArray['sid']}&r={$parsedArray['r']}&e={$parsedArray['e']}&nc={$parsedArray['nc']}&a={$parsedArray['a']}&v={$parsedArray['v']}";
if (!isset($_SESSION['selected_token'])) {
    $_SESSION['selected_token'] = $token;
}

$playurl = "http://gslb.gcable.cn:8070/live/".$n[$id][0].".m3u8".$_SESSION['selected_token'];

if($_GET["playseek"]){//时移，时间参数为年月日时分秒，例子：playseek=20200629193000-20200629204000
    $tms=explode("-",$_GET["playseek"]);//将时间参数的开始和结束分开
    $st=$tms[0];//开始时间
    $et=$tms[1];//结束时间

    $st=strtotime($tms[0]);
    $et=strtotime($tms[1]);

    $wasu=$playurl."&starttime=".$st."&endtime=".$et;
}
else{//直播

    $wasu=$playurl;

}

//header('location:'.urldecode($wasu));
header("location: $wasu");
exit;
?>
