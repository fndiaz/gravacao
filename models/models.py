gravacao_lg = db.define_table("gravacao_lg",
      Field("datetime"),
      Field("acao"),
      Field("pastas"),
      #auth.signature
      format="%(nome)s")

