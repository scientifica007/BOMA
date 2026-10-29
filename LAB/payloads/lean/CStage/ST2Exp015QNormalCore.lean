/- Adapted proof pattern; see ST2-EXP-015_IMPLEMENTATION_PROVENANCE_001.md. -/
/- ST2-EXP-015: independent commutative ring on Route Q's own NormalForm.
No selected pair-route declaration or field producer is referenced. -/
namespace BOMA.C.StageTwo.QNormalCore015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.StageTwo.CauchyOrderCore003
open BOMA.C.StageTwo.ScalarInterface015

open BOMA.C.StageTwo.ScalarConsequences015

/-- The Q-local carrier is Route Q's own canonical normalization record. -/
abbrev QNormal : Type := BOMA.C.StageTwo.QNormalRoute015.NormalForm

/-- The Q-normal identity is record equality, equivalent to coordinate equality. -/
theorem n_ext {z w : QNormal}
    (hre : z.re = w.re) (him : z.im = w.im) : z = w :=
  BOMA.C.StageTwo.QNormalRoute015.normal_ext hre him

def nZero : QNormal := BOMA.C.StageTwo.QNormalRoute015.zero
def nOne : QNormal := BOMA.C.StageTwo.QNormalRoute015.one
def nOfR (a : RCBOMA) : QNormal := BOMA.C.StageTwo.QNormalRoute015.ofR a
def nI : QNormal := BOMA.C.StageTwo.QNormalRoute015.imag
def nNeg (z : QNormal) : QNormal := BOMA.C.StageTwo.QNormalRoute015.neg z
def nAdd (z w : QNormal) : QNormal := BOMA.C.StageTwo.QNormalRoute015.add z w
def nMul (z w : QNormal) : QNormal := BOMA.C.StageTwo.QNormalRoute015.mul z w

/-- Scalar additive reassociation needed by the explicit equational normalizer. -/
theorem r_add_left_comm_from_interface
    (C : CauchyScalarCertificate) (a b c : RCBOMA) :
    rCAdd a (rCAdd b c) = rCAdd b (rCAdd a c) := by
  calc
    rCAdd a (rCAdd b c) = rCAdd (rCAdd a b) c := (C.addAssoc a b c).symm
    _ = rCAdd (rCAdd b a) c := by rw [C.addComm a b]
    _ = rCAdd b (rCAdd a c) := C.addAssoc b a c

/-- Scalar multiplicative reassociation needed by the explicit normalizer. -/
theorem r_mul_left_comm_from_interface
    (C : CauchyScalarCertificate) (a b c : RCBOMA) :
    rCMul a (rCMul b c) =
      rCMul b (rCMul a c) := by
  calc
    rCMul a (rCMul b c) =
        rCMul (rCMul a b) c := (C.mulAssoc a b c).symm
    _ = rCMul (rCMul b a) c := by rw [C.mulComm a b]
    _ = rCMul b (rCMul a c) := C.mulAssoc b a c

/-- Distribution in the first scalar argument is derived, not assumed. -/
theorem r_mul_add_left_from_interface
    (C : CauchyScalarCertificate) (a b c : RCBOMA) :
    rCMul (rCAdd a b) c =
      rCAdd (rCMul a c) (rCMul b c) := by
  calc
    rCMul (rCAdd a b) c = rCMul c (rCAdd a b) :=
      C.mulComm (rCAdd a b) c
    _ = rCAdd (rCMul c a) (rCMul c b) :=
      C.distribRight c a b
    _ = rCAdd (rCMul a c) (rCMul b c) := by
      rw [C.mulComm c a, C.mulComm c b]

/-- Additive inverse distributes over scalar addition using inverse uniqueness. -/
theorem r_neg_add_from_interface
    (C : CauchyScalarCertificate) (a b : RCBOMA) :
    rCNeg (rCAdd a b) = rCAdd (rCNeg a) (rCNeg b) := by
  have h : rCAdd (rCAdd a b) (rCAdd (rCNeg a) (rCNeg b)) = rCZero := by
    calc
      rCAdd (rCAdd a b) (rCAdd (rCNeg a) (rCNeg b)) =
          rCAdd a (rCAdd b (rCAdd (rCNeg a) (rCNeg b))) :=
        C.addAssoc a b (rCAdd (rCNeg a) (rCNeg b))
      _ = rCAdd a (rCAdd (rCNeg a) (rCAdd b (rCNeg b))) := by
        rw [r_add_left_comm_from_interface C b (rCNeg a) (rCNeg b)]
      _ = rCAdd (rCAdd a (rCNeg a)) (rCAdd b (rCNeg b)) :=
        (C.addAssoc a (rCNeg a) (rCAdd b (rCNeg b))).symm
      _ = rCZero := by
        rw [C.addInverseRight a, C.addInverseRight b, C.addZeroLeft rCZero]
  exact (add_inverse_unique_from_interface C h).symm

/-- The canonical complex zero and unit remain distinct. -/
theorem n_zero_ne_one (C : CauchyScalarCertificate) :
    nZero ≠ nOne := by
  intro h
  exact C.nontrivial (congrArg BOMA.C.StageTwo.QExpression015.NormalForm.re h)

/-- The Q-normal real embedding is faithful. -/
theorem n_ofR_injective {a b : RCBOMA} (h : nOfR a = nOfR b) : a = b :=
  BOMA.C.StageTwo.QNormalRoute015.ofR_injective h

theorem n_add_comm (C : CauchyScalarCertificate) (z w : QNormal) :
    nAdd z w = nAdd w z := by
  apply n_ext
  · exact C.addComm z.re w.re
  · exact C.addComm z.im w.im

theorem n_add_assoc
    (C : CauchyScalarCertificate) (z w v : QNormal) :
    nAdd (nAdd z w) v = nAdd z (nAdd w v) := by
  apply n_ext
  · exact C.addAssoc z.re w.re v.re
  · exact C.addAssoc z.im w.im v.im

theorem n_add_zero_left (C : CauchyScalarCertificate) (z : QNormal) :
    nAdd nZero z = z := by
  apply n_ext
  · exact C.addZeroLeft z.re
  · exact C.addZeroLeft z.im

theorem n_add_zero_right (C : CauchyScalarCertificate) (z : QNormal) :
    nAdd z nZero = z := by
  rw [n_add_comm C z nZero, n_add_zero_left C z]

theorem n_add_neg_right (C : CauchyScalarCertificate) (z : QNormal) :
    nAdd z (nNeg z) = nZero := by
  apply n_ext
  · exact C.addInverseRight z.re
  · exact C.addInverseRight z.im

theorem n_add_neg_left (C : CauchyScalarCertificate) (z : QNormal) :
    nAdd (nNeg z) z = nZero := by
  rw [n_add_comm C (nNeg z) z, n_add_neg_right C z]

theorem n_neg_involutive (C : CauchyScalarCertificate) (z : QNormal) :
    nNeg (nNeg z) = z := by
  apply n_ext
  · exact neg_involutive_from_interface C z.re
  · exact neg_involutive_from_interface C z.im

theorem n_mul_comm (C : CauchyScalarCertificate) (z w : QNormal) :
    nMul z w = nMul w z := by
  cases z <;> cases w <;>
    simp [nMul, BOMA.C.StageTwo.QNormalRoute015.mul, BOMA.C.StageTwo.QExpression015.nfMul, C.mulComm, C.addComm]

/-- Associativity is an explicit consequence of the fixed Cauchy real ring laws. -/
theorem n_mul_assoc
    (C : CauchyScalarCertificate) (z w v : QNormal) :
    nMul (nMul z w) v = nMul z (nMul w v) := by
  cases z <;> cases w <;> cases v <;>
    simp [nMul, BOMA.C.StageTwo.QNormalRoute015.mul, BOMA.C.StageTwo.QExpression015.nfMul,
      r_mul_add_left_from_interface C, C.distribRight,
      mul_neg_left_from_interface C, mul_neg_right_from_interface C,
      r_neg_add_from_interface C, neg_involutive_from_interface C,
      C.mulAssoc, C.mulComm, r_mul_left_comm_from_interface C,
      C.addAssoc, C.addComm, r_add_left_comm_from_interface C]

theorem n_mul_one_left (C : CauchyScalarCertificate) (z : QNormal) :
    nMul nOne z = z := by
  apply n_ext
  · change
      rCAdd (rCMul rCOne z.re)
        (rCNeg (rCMul rCZero z.im)) = z.re
    rw [C.mulOneLeft z.re, mul_zero_left_from_interface C z.im,
      neg_zero_from_interface C,
      BOMA.C.StageTwo.QNormalRoute015.add_zero_right_from_interface C z.re]
  · change
      rCAdd (rCMul rCOne z.im)
        (rCMul rCZero z.re) = z.im
    rw [C.mulOneLeft z.im, mul_zero_left_from_interface C z.re,
      BOMA.C.StageTwo.QNormalRoute015.add_zero_right_from_interface C z.im]

theorem n_mul_one_right (C : CauchyScalarCertificate) (z : QNormal) :
    nMul z nOne = z := by
  rw [n_mul_comm C z nOne, n_mul_one_left C z]

/-- Right distribution is proved independently from the abstract real interface. -/
theorem n_mul_add_right
    (C : CauchyScalarCertificate) (z w v : QNormal) :
    nMul z (nAdd w v) = nAdd (nMul z w) (nMul z v) := by
  cases z <;> cases w <;> cases v <;>
    simp [nMul, nAdd, BOMA.C.StageTwo.QNormalRoute015.mul, BOMA.C.StageTwo.QExpression015.nfMul,
      BOMA.C.StageTwo.QNormalRoute015.add, BOMA.C.StageTwo.QExpression015.nfAdd,
      r_mul_add_left_from_interface C, C.distribRight,
      mul_neg_left_from_interface C, mul_neg_right_from_interface C,
      r_neg_add_from_interface C, neg_involutive_from_interface C,
      C.mulAssoc, C.mulComm, r_mul_left_comm_from_interface C,
      C.addAssoc, C.addComm, r_add_left_comm_from_interface C]

theorem n_mul_add_left
    (C : CauchyScalarCertificate) (z w v : QNormal) :
    nMul (nAdd z w) v = nAdd (nMul z v) (nMul w v) := by
  calc
    nMul (nAdd z w) v = nMul v (nAdd z w) :=
      n_mul_comm C (nAdd z w) v
    _ = nAdd (nMul v z) (nMul v w) := n_mul_add_right C v z w
    _ = nAdd (nMul z v) (nMul w v) := by
      rw [n_mul_comm C v z, n_mul_comm C v w]

theorem n_mul_zero_left (C : CauchyScalarCertificate) (z : QNormal) :
    nMul nZero z = nZero := by
  apply n_ext
  · change
      rCAdd (rCMul rCZero z.re)
        (rCNeg (rCMul rCZero z.im)) = rCZero
    rw [mul_zero_left_from_interface C z.re,
      mul_zero_left_from_interface C z.im,
      neg_zero_from_interface C, C.addZeroLeft rCZero]
  · change
      rCAdd (rCMul rCZero z.im)
        (rCMul rCZero z.re) = rCZero
    rw [mul_zero_left_from_interface C z.im,
      mul_zero_left_from_interface C z.re, C.addZeroLeft rCZero]

theorem n_mul_zero_right (C : CauchyScalarCertificate) (z : QNormal) :
    nMul z nZero = nZero := by
  rw [n_mul_comm C z nZero, n_mul_zero_left C z]

theorem n_ofR_zero : nOfR rCZero = nZero := rfl

theorem n_ofR_one : nOfR rCOne = nOne := rfl

theorem n_ofR_neg (C : CauchyScalarCertificate) (a : RCBOMA) :
    nOfR (rCNeg a) = nNeg (nOfR a) := by
  apply n_ext
  · rfl
  · exact (neg_zero_from_interface C).symm

theorem n_ofR_add (C : CauchyScalarCertificate) (a b : RCBOMA) :
    nOfR (rCAdd a b) = nAdd (nOfR a) (nOfR b) := by
  apply n_ext
  · rfl
  · exact (C.addZeroLeft rCZero).symm

theorem n_ofR_mul (C : CauchyScalarCertificate) (a b : RCBOMA) :
    nOfR (rCMul a b) = nMul (nOfR a) (nOfR b) := by
  apply n_ext
  · change
      rCMul a b =
        rCAdd (rCMul a b) (rCNeg (rCMul rCZero rCZero))
    rw [mul_zero_left_from_interface C rCZero,
      neg_zero_from_interface C,
      BOMA.C.StageTwo.QNormalRoute015.add_zero_right_from_interface C
        (rCMul a b)]
  · change
      rCZero = rCAdd (rCMul a rCZero) (rCMul rCZero b)
    rw [mul_zero_right_from_interface C a,
      mul_zero_left_from_interface C b, C.addZeroLeft rCZero]

theorem n_i_squared (C : CauchyScalarCertificate) :
    nMul nI nI = nNeg nOne :=
  BOMA.C.StageTwo.QNormalRoute015.imag_squared C

theorem n_generation (C : CauchyScalarCertificate) (z : QNormal) :
    ∃ a b : RCBOMA, z = nAdd (nOfR a) (nMul (nOfR b) nI) :=
  BOMA.C.StageTwo.QNormalRoute015.decomposition C z

theorem n_coordinate_unique
    (C : CauchyScalarCertificate) {a b a' b' : RCBOMA}
    (h : nAdd (nOfR a) (nMul (nOfR b) nI) =
      nAdd (nOfR a') (nMul (nOfR b') nI)) :
    a = a' ∧ b = b' :=
  BOMA.C.StageTwo.QNormalRoute015.decomposition_unique C h

theorem n_i_not_real (C : CauchyScalarCertificate) :
    ¬ ∃ a : RCBOMA, nI = nOfR a :=
  BOMA.C.StageTwo.QNormalRoute015.imag_not_real C

/-- Precisely scoped Q-normal integration surface: ring, not field. -/
structure QNormalRingCertificate where
  nontrivial : nZero ≠ nOne
  embeddingInjective : ∀ {a b : RCBOMA}, nOfR a = nOfR b → a = b
  addComm : ∀ z w : QNormal, nAdd z w = nAdd w z
  addAssoc : ∀ z w v : QNormal, nAdd (nAdd z w) v = nAdd z (nAdd w v)
  addZeroLeft : ∀ z : QNormal, nAdd nZero z = z
  addInverseRight : ∀ z : QNormal, nAdd z (nNeg z) = nZero
  mulComm : ∀ z w : QNormal, nMul z w = nMul w z
  mulAssoc : ∀ z w v : QNormal, nMul (nMul z w) v = nMul z (nMul w v)
  mulOneLeft : ∀ z : QNormal, nMul nOne z = z
  distribRight : ∀ z w v : QNormal,
    nMul z (nAdd w v) = nAdd (nMul z w) (nMul z v)
  mulZeroRight : ∀ z : QNormal, nMul z nZero = nZero
  embeddingZero : nOfR rCZero = nZero
  embeddingOne : nOfR rCOne = nOne
  embeddingNeg : ∀ a : RCBOMA, nOfR (rCNeg a) = nNeg (nOfR a)
  embeddingAdd : ∀ a b : RCBOMA,
    nOfR (rCAdd a b) = nAdd (nOfR a) (nOfR b)
  embeddingMul : ∀ a b : RCBOMA,
    nOfR (rCMul a b) = nMul (nOfR a) (nOfR b)
  imagSquared : nMul nI nI = nNeg nOne
  generation : ∀ z : QNormal,
    ∃ a b : RCBOMA, z = nAdd (nOfR a) (nMul (nOfR b) nI)
  coordinateUnique : ∀ {a b a' b' : RCBOMA},
    nAdd (nOfR a) (nMul (nOfR b) nI) =
      nAdd (nOfR a') (nMul (nOfR b') nI) → a = a' ∧ b = b'
  imagNotReal : ¬ ∃ a : RCBOMA, nI = nOfR a

/-- Abstract real-interface construction; no real representation is unfolded. -/
theorem qNormalRingCertificate
    (C : CauchyScalarCertificate) : QNormalRingCertificate where
  nontrivial := n_zero_ne_one C
  embeddingInjective := @n_ofR_injective
  addComm := n_add_comm C
  addAssoc := n_add_assoc C
  addZeroLeft := n_add_zero_left C
  addInverseRight := n_add_neg_right C
  mulComm := n_mul_comm C
  mulAssoc := n_mul_assoc C
  mulOneLeft := n_mul_one_left C
  distribRight := n_mul_add_right C
  mulZeroRight := n_mul_zero_right C
  embeddingZero := n_ofR_zero
  embeddingOne := n_ofR_one
  embeddingNeg := n_ofR_neg C
  embeddingAdd := n_ofR_add C
  embeddingMul := n_ofR_mul C
  imagSquared := n_i_squared C
  generation := n_generation C
  coordinateUnique := @n_coordinate_unique C
  imagNotReal := n_i_not_real C

/-- Instantiate the ring-core certificate on the accepted Stage-One real export. -/
theorem qNormalRingCertificateFromCauchyR : QNormalRingCertificate :=
  qNormalRingCertificate cauchyScalarCertificate

end BOMA.C.StageTwo.QNormalCore015
