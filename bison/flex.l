%{
	#include "y.tab.h"	
%}
%option noyywrap
%%

[a-zA-Z] {yylval.character = yytext[0];  return LETTER;}

"+" return '+';
"*" return '*';
"(" return '(';
")" return ')';

\n {return EOL;}

. {yyerror("Illegal char"); return yytext[0];}

%%