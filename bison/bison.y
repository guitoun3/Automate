%{
	#include <stdio.h>		
	#include <string.h>
%}

%union {
	char character;
	char* str;
}

%type <str> expr

%token <character> LETTER
%token EOL
%left '+'
%left LETTER CONCAT
%nonassoc '*'
%nonassoc '('

%%
input: /* empty */
	| line input
	;

line: expr EOL	{printf("\nExpression accepted : %s\n", $1);}
	| error EOL	{printf("\nExpression rejected\n");}
	;

expr: LETTER 					{char* s = malloc(3 * sizeof(char));
								sprintf(s, "\"%c\"", $1);
								$$ = s;}
	| expr expr %prec CONCAT	{char* s = malloc(2 * sizeof(char*) + 10 * sizeof(char));
								sprintf(s, "[\".\", [%s, %s]]", $1, $2);
								$$ = s;}
	| expr '+'  expr 			{char* s = malloc(2 * sizeof(char*) + 10 * sizeof(char));
								sprintf(s, "[\"+\", [%s, %s]]", $1, $3);
								$$ = s;}
	| '(' expr ')'				{$$ = $2;}
	| expr '*'					{char* s = malloc(sizeof(char*) + 9 * sizeof(char));
								sprintf(s, "[\"*\", [%s]]", $1);
								$$ = s;}
	;

%%

yyerror(char* msg){
	printf("%s\n", msg);
}

int main(int argc, char *argv[]){
	yyparse();

	return 0;
}