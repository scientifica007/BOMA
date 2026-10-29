/- ST2-EXP-016 Gate B/C: research-only algebraic norm nondegeneracy.
   Single replacement of the production orderTotal field by the one
   frozen NormAnisotropy016 condition. This does NOT claim field or
   integration closure; those are later Gate D obligations.
   No global inverse selector, new axiom, or selected C proof import. -/
namespace BOMA.C.StageTwo.NormAnisotropy016

open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindNegationCandidate001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.C.StageTwo.TotalOrderRegime004.WithoutOrderTotal

/-- Fifteen fixed Gate-E laws and exactly one new algebraic replacement.
    An explicit certificate parameter is not a new foundational axiom. -/
structure RNormAnisotropyCertificate016 where
  scalar : RWithoutOrderTotalCertificate
  normAnisotropy : ∀ a b : RBOMA,
    rAdd (rMulCandidate a a) (rMulCandidate b b) = rZero →
      a = rZero ∧ b = rZero

/-- Exactly the Gate-E Route-P sum-of-two-squares norm. -/
def norm016 (z : Pair004) : RBOMA :=
  rAdd (rMulCandidate z.re z.re) (rMulCandidate z.im z.im)

/-- The single frozen condition gives both zero coordinates, directly. -/
theorem normZeroCoordinates016
    (C : RNormAnisotropyCertificate016)
    (z : Pair004) (hn : norm016 z = rZero) :
    z.re = rZero ∧ z.im = rZero := by
  exact C.normAnisotropy z.re z.im hn

/-- Zero norm forces zero pair; no totality or nonnegative-square lemma. -/
theorem normZeroForcesZero016
    (C : RNormAnisotropyCertificate016)
    (z : Pair004) (hn : norm016 z = rZero) :
    z = zero004 := by
  rcases normZeroCoordinates016 C z hn with ⟨hre, him⟩
  exact pair_ext004 hre him

/-- The constructive nonzero norm bridge needed by the inverse proof. -/
theorem normNonzero016
    (C : RNormAnisotropyCertificate016)
    {z : Pair004} (hz : z ≠ zero004) :
    norm016 z ≠ rZero := by
  intro hn
  exact hz (normZeroForcesZero016 C z hn)

/-- The old fifteen-field scalar inverse witness now applies to the norm.
    This supplies a scalar witness, not yet a verified complex inverse. -/
theorem normScalarInverseExists016
    (C : RNormAnisotropyCertificate016)
    {z : Pair004} (hz : z ≠ zero004) :
    ∃ t : RBOMA, rMulCandidate (norm016 z) t = rOne := by
  exact C.scalar.inverseExists (norm016 z) (normNonzero016 C hz)

/-- B reuses the exact unchanged seven-Claim Gate-E proof package.
    C establishes the algebraic norm bridge separately. -/
structure NormBridgeCertificate016
    (C : RNormAnisotropyCertificate016) : Prop where
  sevenControls : CSurvivorCertificate004 C.scalar
  normZeroCoordinates : ∀ z : Pair004,
    norm016 z = rZero → z.re = rZero ∧ z.im = rZero
  normNonzero : ∀ z : Pair004, z ≠ zero004 → norm016 z ≠ rZero
  scalarInverseWitness : ∀ z : Pair004, z ≠ zero004 →
    ∃ t : RBOMA, rMulCandidate (norm016 z) t = rOne

/-- Independent research-only B/C checkpoint; not C-CL-FIELD-001 PASS. -/
theorem normBridgeCertificate016
    (C : RNormAnisotropyCertificate016) :
    NormBridgeCertificate016 C where
  sevenControls := cSurvivorCertificate004 C.scalar
  normZeroCoordinates := normZeroCoordinates016 C
  normNonzero := fun _ hz => normNonzero016 C hz
  scalarInverseWitness := fun _ hz => normScalarInverseExists016 C hz

end BOMA.C.StageTwo.NormAnisotropy016
