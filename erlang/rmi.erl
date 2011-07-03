-module(rmi).

-compile(export_all).

-import(lists, [reverse/1, foreach/2]).
-import(string, [tokens/2, strip/2]).


start(Callback, Host, ObjectName, ClassName) -> 
    spawn(register_with_morb(Host, 9765, Callback, ObjectName, ClassName)).

register_with_morb(HostName, Port, Callback, ObjectName, ClassName) ->
	case gen_tcp:connect(HostName, Port, [binary, {packet, 0}]) of
	{ok, Socket} ->
		ok = gen_tcp:send(Socket, "ORB RegistrationAgent Register ClassName:"++ClassName++" ObjectName:"++ObjectName++"\n"),
		receive_data(Callback, Socket);
	{error, Reason} ->
		io:format("Failed to open socket~n~p~n",[Reason])
	end.


receive_data(Callback, Socket) ->
    receive
        {rmi_send, Object, Class, Call, Args} ->
            AsString = fun(X) -> " ~p"++X end,
            io:format("~p~n", [Args]),
            ok = gen_tcp:send(Socket, Object++" "++Class++" "++Call++" "++Args++" "++"\n"),
			receive_data(Callback, Socket);
		{tcp, Socket, Bin} ->
			List = tokens(binary_to_list(Bin), "\s"),
            %%io:format("Got list~p~n",[List]),
			[ObjectName|L1] = List,
			[ClassName|L2] = L1,
			[Call|L3] = L2,
			[Args] = tokens(L3, ":"),
            KWargs = [tokens(K, ":") || K <- Args],
            try apply(Callback, list_to_atom(Call), KWargs)
            catch
                _:_ -> apply(Callback, catchAll, [Call, KWargs])
			end,
            receive_data(Callback, Socket)
            
	end.