; Test macros

DWA     MACRO WHERE
        DB   (WHERE >> 8) + 128
        DB   WHERE & 0FFH
        ENDM


TAB1:
        DB   "LIST"
        DWA  LIST
        DB   "RUN"
        DWA  RUN
        DB   "NEW"
        DWA  NEW
