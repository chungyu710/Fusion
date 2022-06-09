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

OBJ := $(addprefix $(ART)/, $(OBJ))

BIN := $(BIN).hex

# ======= CREATE ARTIFACTS DIRECTORY ======= #

ifneq ($(DIR), )
$(shell mkdir -p $(addprefix $(ART)/, $(DIR)))
else
$(shell mkdir -p $(ART))
endif

# ======= LINK ======= #

$(ART)/$(BIN): $(OBJ)
	@echo "LD   $^"
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
	@echo "RM   $(ART)/"
	@rm -rf $(ART)
