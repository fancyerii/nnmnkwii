# coding: utf-8
from nnmnkwii.io import hts
from nnmnkwii.frontend import merlin as fe
from os.path import dirname, join
import copy
from nnmnkwii.util import example_question_file
import re

DATA_DIR = join(dirname(__file__), "data")

def test_load_question_set():
    binary_dict, continuous_dict = hts.load_question_set(example_question_file())
    assert len(binary_dict) + len(continuous_dict) == 416

def test_htk_style_question_basics():
    binary_dict, continuous_dict = hts.load_question_set(join(DATA_DIR, "test_question.hed"))
    # sil k o n i ch i w a sil
    input_phone_label = join(DATA_DIR, "hts-nit-atr503", "phrase01.lab")
    labels = hts.load(input_phone_label)

    # For reference
    """
    -1 -1 xx^xx-sil+k=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:5_5%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:1_5/K:1+1-5
    -1 -1 xx^sil-k+o=N/A:-4+1+5/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 sil^k-o+N=n/A:-4+1+5/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 k^o-N+n=i/A:-3+2+4/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 o^N-n+i=ch/A:-2+3+3/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 N^n-i+ch=i/A:-2+3+3/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 n^i-ch+i=w/A:-1+4+2/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 i^ch-i+w=a/A:-1+4+2/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 ch^i-w+a=sil/A:0+5+1/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 i^w-a+sil=xx/A:0+5+1/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx_xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
    -1 -1 w^a-sil+xx=xx/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:xx+xx_xx/E:5_5!0_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:xx_xx%xx_xx_xx/H:1_5/I:xx-xx@xx+xx&xx-xx|xx+xx/J:xx_xx/K:1+1-5
    """

    # Test if we can handle wildcards correctly
    # also test basic phon contexts (LL, L, C, R, RR)
    """
    QS "LL-Phone_Muon1"     {sil^,pau^}    # without wildcards
    QS "LL-Phone_Muon2"     {sil^*,pau^*}  # with wildcards, should be equivalent with above
    QS "L-Phone_Muon1"      {*^sil-*,*^pau-*}
    QS "C-Phone_sil"        {*-sil+*}
    QS "R-Phone_o"          {*+o=*}
    QS "RR-Phone_o"         {*=o/A:*}
    """
    LL_muon1 = binary_dict[0][0]
    LL_muon2 = binary_dict[1][0]
    L_muon1 = binary_dict[2][0]
    C_sil = binary_dict[3][0]
    R_phone_o = binary_dict[4][0]
    RR_phone_o = binary_dict[5][0]

    # xx^xx-sil+k=o
    label = labels[0][-1]
    assert LL_muon1.search(label) is None
    assert LL_muon2.search(label) is None
    assert L_muon1.search(label) is None
    assert C_sil.search(label)
    assert R_phone_o.search(label) is None
    assert RR_phone_o.search(label)

    # xx^sil-k+o=N
    label = labels[1][-1]
    assert LL_muon1.search(label) is None
    assert LL_muon2.search(label) is None
    assert L_muon1.search(label)
    assert C_sil.search(label) is None
    assert R_phone_o.search(label)
    assert RR_phone_o.search(label) is None

    # sil^k-o+N=n
    label = labels[2][-1]
    assert LL_muon1.search(label)
    assert LL_muon2.search(label)
    assert L_muon1.search(label) is None
    assert C_sil.search(label) is None
    assert R_phone_o.search(label) is None
    assert RR_phone_o.search(label) is None

def test_state_alignment_label_file():
    input_state_label = join(DATA_DIR, "label_state_align", "arctic_a0001.lab")
    labels = hts.load(input_state_label)
    with open(input_state_label) as f:
        assert f.read() == str(labels)

    print(labels.num_states())
    assert labels.num_states() == 5

    # Get and restore durations
    durations = fe.duration_features(labels)
    labels_copy = copy.deepcopy(labels)
    labels_copy.set_durations(durations)

    assert str(labels) == str(labels_copy)


def test_phone_alignment_label():
    input_state_label = join(DATA_DIR, "label_phone_align", "arctic_a0001.lab")
    labels = hts.load(input_state_label)
    assert not labels.is_state_alignment_label()

def test_label_without_times():
    input_phone_label = join(DATA_DIR, "hts-nit-atr503", "phrase01.lab")
    labels = hts.load(input_phone_label)
    assert not labels.is_state_alignment_label()
