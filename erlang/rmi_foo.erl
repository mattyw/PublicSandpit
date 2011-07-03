-module(rmi_foo).

-define(RMI, rmi).

-compile(export_all).

-import(rmi).


start() ->
    Pid = spawn(rmi, start, [rmi_foo, "erl", "Erlang"]),
	erlang:register(?RMI, Pid).

hello(A, B, From) ->
    [_, AV] = A,
	[_, BV] = B,
    io:format("rmi_foo:hello ~p ~p~n", [AV, BV]),
	send_hello().


catchAll(Call) ->
    io:format("Caught invalid call ~p~n",[Call]).


send_hello() ->
    ?RMI ! {rmi_send, "erl1", "Erlang1", "hello", "One:C Two:D"}.