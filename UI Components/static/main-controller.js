var app = angular.module('search');

app.controller('mainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.message = "Hello there!";
    
    var obj = {
        poi_name: $scope.poi_name,
        from_date: $scope.tweet_date_f,
        to_date: $scope.tweet_date_t,
        on_this_date: $scope.tweet_date_o,
        hashtags: $scope.hashtags,
        mentions: $scope.user_mentions,
        url: $scope.tweet_urls,
        lang_e: $scope.lang_e,
        lang_p: $scope.lang_p,
        lang_h: $scope.lang_h              

    };
	
	$scope.searchQuery = function() {
		$http.get('http://192.168.1.55:5000/query?q='+$scope.queryterm).then(function(res) {
			$scope.tweets = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.analyzeTweets = function() {
		var ids = [];
		for(var t in $scope.tweets) {
			ids.push($scope.tweets[t].id);
		}
		$http.post('http://192.168.1.55:5000/replies', {
			query: $scope.queryterm
		}).then(function(res) {
			alert(JSON.stringify(res.data));
		}, function(err) {
			$scope.message = "this is error";
		});
	};
}]);
