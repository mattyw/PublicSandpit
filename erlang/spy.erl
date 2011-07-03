-module (spy).

-compile(export_all).

-define(SPY, spy).

-import(rmi).

start() ->
	Pid = spawn(rmi, start, [spy, "127.0.0.1", "Spy", "RMISpy"]),
	erlang:register(?SPY, Pid).

catchAll(Call, Kwargs) ->
	io:format("~p~p~n",[Call, Kwargs]).