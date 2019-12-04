var app = angular.module('search');

app.controller('mainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.message = "Hello there!";
	$scope.tweetsCount = 0;
	var tweetReport = {},
		repliesReport = {};
	$scope.poiOptions = [	
			{ twhandle: "AmitShah", label: "Amit Shah" },
			{ twhandle: "smritiirani", label: "Smriti Irani" },
			{ twhandle: "narendramodi", label: "Narendra Modi" },
			{ twhandle: "rajnathsingh", label: "Rajnath Singh" },
			{ twhandle: "myogiadityanath", label: "Yogi Adityanath" },
			{ twhandle: "dilmabr", label: "Dilma Rousseff" },
			{ twhandle: "jairbolsonaro", label: "Jair M. Bolsonaro" },
			{ twhandle: "joseserra_", label: "José Serra" },
			{ twhandle: "MarinaSilva", label: "Marina Silva" },
			{ twhandle: "cirogomes", label: "Ciro Gomes" },
			{ twhandle: "BernieSanders", label: "Bernie Sanders" },
			{ twhandle: "HillaryClinton", label: "Hillary Clinton" },
			{ twhandle: "Mike_Pence", label: "Mike pence" },
			{ twhandle: "BarackObama", label: "Barack Obama" },
			{ twhandle: "realdonaldtrump", label: "Donald J. trump" }
		];
	$scope.hashtagOptions = [
	  "presidentkovind",
	  "ciro12",
	  "morningnutrition",
	  "actonclimate",
	  "mannkibaat",
	  "हिंदी_दिवस",
	  "aovivo",
	  "pelademocracia",
	  "cirosim",
	  "cironorodaviva",
	  "sotu",
	  "fatoseversoes",
	  "doyourjob",
	  "maga",
	  "getcovered",
	  "stophindiimposition",
	  "cironaglobo",
	  "tsunamiciro",
	  "hindidiwas",
	  "cironaglobonews",
	  "demdebate",
	  "stophindiimperialism",
	  "obamacare",
	  "debatenight",
	  "yogaday2019",
	  "chandrayaan2",
	  "apollo50th",
	  "dragon",
	  "debateaparecida",
	  "icymi",
	  "artemis",
	  "crewdragon",
	  "cironacnbb",
	  "cironarecord",
	  "immigrationaction",
	  "lulalivre",
	  "gendunford",
	  "indiana",
	  "isro",
	  "ciropresidente",
	  "engineersday",
	  "india",
	  "poshanmaah2019",
	  "votemarina18",
	  "projetoanticrime",
	  "vpdebate",
	  "ovotonarecord",
	  "uolnasurnas",
	  "modified100",
	  "transformingindia",
	  "irandeal",
	  "debatesbt",
	  "debate",
	  "budgetfornewindia",
	  "vikaskabudget",
	  "cygnus",
	  "serra456",
	  "fatoseversões",
	  "kashmir",
	  "knowyourmil",
	  "periscope",
	  "scotus",
	  "gazetaestadaojp",
	  "rio2016",
	  "serrasenador",
	  "lutarsempre",
	  "chegadeagrotóxicos",
	  "raisethewage",
	  "usmca",
	  "teamrajnivas",
	  "g20",
	  "secdef",
	  "abhoganyay",
	  "medicareforall",
	  "dyk",
	  "otd",
	  "poshanabhiyaan",
	  "dod",
	  "dorian",
	  "gst",
	  "standwithhongkong",
	  "trumppence16",
	  "தமிழ்வாழ்க",
	  "cironaredetv",
	  "hurricanedorian",
	  "leadontrade",
	  "newindia",
	  "pergunteaociro",
	  "servicemembers",
	  "zikazero",
	  "electionsonmyplate",
	  "pec215nao",
	  "हिन्दीदिवस",
	  "bernie2020",
	  "pergunteaociro12",
	  "ultimathule",
	  "apollo11",
	  "astatethatworks",
	  "bebest",
	  "fitindiamovement"
	];
	
	$scope.updatePoi = function(poi) {
		$scope.poi_name = poi.twhandle;
	};
	
	$scope.updateHashtag = function(hashtag) {
		$scope.hashtag = hashtag;
	};
	
	$scope.searchQuery = function() {
		$http.get('/query?q='+$scope.queryterm).then(function(res) {
			var fdate = document.getElementById('from-date').value,
				tdate = document.getElementById('to-date').value;
			var radios = document.getElementsByName('twlang');
			var lang = 'en';
			for(var radEl in radios) {
				if(radios[radEl].checked) {
					lang = radios[radEl].value;
					break;
				}
			}
			var obj = {
				poi_name: $scope.poi_name ? $scope.poi_name : 'All',
				tweet_date: '[' + fdate + ' TO ' + tdate + ']',
				hashtags: $scope.hashtag,
				lang: lang
			};
			$scope.tweets = res.data.tweets;
			$scope.tweetsCount = res.data.count;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.analyzeTweets = function() {
		$scope.openModal();
		$http.post('/queryanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			queryAnalysisReport = res.data;			
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.openModal = function() {
		$('#exampleModalLong').modal('show');
	};
	
	$('#exampleModalLong').on('shown.bs.modal', function () {
			google.charts.load('current', {'packages':['corechart']});
			google.charts.setOnLoadCallback(drawTweetChart);
			function drawTweetChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', queryAnalysisReport.tweet.pos],
					['Negative', queryAnalysisReport.tweet.neg],
					['Neutral', queryAnalysisReport.tweet.neut]
				]);
				var options = {'title':'Sentiment Analysis on Search Query topic over Tweets', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('tweet-analysis'));
				chart.draw(data, options);
			}
			google.charts.setOnLoadCallback(drawRepliesChart);
			function drawRepliesChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', queryAnalysisReport.replies.pos],
					['Negative', queryAnalysisReport.replies.neg],
					['Neutral', queryAnalysisReport.replies.neut]
				]);
				var options = {'title':'Sentiment Analysis on overall replies to the topic', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('replies-analysis'));
				chart.draw(data, options);
			}
		});
}]);
