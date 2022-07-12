# ======= IMPORT CONFIGURATION ======= #

include config.mk

# ======= VERIFY CONFIGURATION ======= #

ifeq ($(CC), )
$(error CC was not specified)
endif

ifeq ($(ART), )
$(error ART was not specified)
endif

ifeq ($(BIN), )
$(error BIN was not specified)
endif

# ======= PROCESS CONFIGURATION ======= #

FLAGS += -I .
SRC += $(wildcard *.c)

ifneq ($(DIR), )
VPATH += $(DIR)
FLAGS += $(addprefix -I , $(DIR))
SRC += $(wildcard $(addsuffix /*.c, $(DIR)))
endif

OBJ := $(SRC:.c=.p1)
DEP := $(SRC:.c=.d)

BIN := $(BIN).hex

# ======= CREATE ARTIFACTS DIRECTORY ======= #

ifneq ($(MAKECMDGOALS), clean)
ifneq ($(DIR), )
$(shell mkdir -p $(addprefix $(ART)/, $(DIR)))
else
$(shell mkdir -p $(ART))
endif
endif

# ======= LINK ======= #

$(ART)/$(BIN): $(addprefix $(ART)/, $(OBJ))
	@echo "LD"
	@echo "$(OBJ)"
	@$(CC) $(LIBS) $(FLAGS) $^ -o $@
	@echo "BIN  $@"

# ======= COMPILE ======= #

$(ART)/%.p1: %.c
	@echo "CC   $<"
	@$(CC) $(FLAGS) -c $< -o $@

# ======= GENERATE DEPENDENCIES ======= #

$(ART)/%.d: %.c
	@$(CC) $(FLAGS) -MM $< -MF $@
	@mv $(subst .c,.i,$(notdir $<)) $(ART)

ifneq ($(MAKECMDGOALS), clean)
-include $(addprefix $(ART)/, $(DEP))
endif

# ======= CLEAN ======= #

clean:
	@echo "RM"
	@echo "$(wildcard $(ART)/**)"
	@rm -rf $(ART)
