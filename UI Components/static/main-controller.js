var app = angular.module('search');

app.controller('mainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.message = "Hello there!";
	
	$scope.searchQuery = function() {
		$http.get('http://192.168.1.55:5000/query?q='+$scope.queryterm).then(function(res) {
			$scope.tweets = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
}]);